import json
import re
from functools import partial

import pytest
from fastapi.testclient import TestClient

from app.agent.service import TravelService
from app.api.travel import get_travel_service
from app.core.config import PROJECT_ROOT
from app.main import app
from app.tools.candidate_providers import (
    CandidateProviderError,
    MockFixtureProvider,
    create_candidate_provider,
)
from app.tools.contracts import SearchInput
from app.tools.mock import (
    run_tool,
    search_attractions,
    search_hotels,
    search_restaurants,
    search_transport,
)

MANIFEST = PROJECT_ROOT / "data/travel/snapshots/openstreetmap/migration_manifest.json"
ROUTES = [
    (route["city"], route["category"])
    for route in json.loads(MANIFEST.read_text(encoding="utf-8"))["routes"]
]
CITIES = [
    ("New York City", 520),
    ("Chicago", 433),
    ("Washington DC", 445),
    ("Miami", 456),
    ("Denver", 411),
    ("Seattle", 466),
    ("San Francisco", 536),
    ("Los Angeles", 495),
    ("Las Vegas", 415),
]
SEARCH = {
    "attractions": search_attractions,
    "hotel": search_hotels,
    "food": search_restaurants,
}


@pytest.fixture(scope="module")
def migrated_provider():
    return create_candidate_provider("snapshot", MANIFEST)


def test_final_manifest_has_every_supported_poi_route(migrated_provider):
    assert len(migrated_provider.routes) == 36


def test_final_manifest_has_globally_unique_identities_and_complete_provenance(migrated_provider):
    rows = [
        row
        for (city, category), provider in migrated_provider.routes.items()
        for row in provider.candidates(city, category)
    ]

    assert len({row.id for row in rows}) == len(rows)
    assert len({(row.provider, row.provider_place_id) for row in rows}) == len(rows)
    assert all(row.cost_origin == "planner_estimate" and row.cost_version == "phase_o_v1" for row in rows)
    assert all(row.snapshot_version and row.snapshot_fetched_at for row in rows)


@pytest.mark.parametrize("city,category", ROUTES)
def test_every_declared_route_fails_closed_when_its_snapshot_is_missing(
    city, category, tmp_path
):
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for route in manifest["routes"]:
        route["snapshot"] = str((MANIFEST.parent / route["snapshot"]).resolve())
        if (route["city"], route["category"]) == (city, category):
            route["snapshot"] = str(tmp_path / "missing.json")
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", path)


@pytest.mark.parametrize("city,_", CITIES)
@pytest.mark.parametrize("category", ["attractions", "hotel", "food"])
def test_batch_snapshots_preserve_controlled_semantics_and_add_real_facts(
    city, _, category, migrated_provider
):
    request = SearchInput(destination=city)
    actual = SEARCH[category](request, migrated_provider)
    expected = SEARCH[category](request, MockFixtureProvider())

    assert actual.source == "snapshot"
    assert [
        (row.id, row.price, row.currency, row.unit, row.tags) for row in actual.data
    ] == [
        (row.id, row.price, row.currency, row.unit, row.tags) for row in expected.data
    ]
    assert len(actual.data) == 3
    assert all(row.provider == "openstreetmap" and row.source == "real_snapshot" for row in actual.data)
    assert all(re.fullmatch(r"(node|way|relation)/[1-9][0-9]*", row.provider_place_id) for row in actual.data)
    assert all(row.address and row.latitude is not None and row.longitude is not None for row in actual.data)
    assert all(row.provider_category_ids and row.snapshot_version for row in actual.data)
    assert all(row.rating is None and row.review_count is None for row in actual.data)


@pytest.mark.parametrize("city,_", CITIES)
def test_batch_transport_remains_controlled_mock(city, _, migrated_provider):
    request = SearchInput(destination=city)
    actual = search_transport(request, migrated_provider)
    expected = search_transport(request, MockFixtureProvider())

    assert actual.source == "mock"
    assert actual.data == expected.data
    assert all(row.provider is None and row.source == "controlled_mock_fixture" for row in actual.data)


@pytest.mark.parametrize("city,expected_total", CITIES)
def test_batch_public_api_preserves_budget_selection_and_validation(
    city, expected_total, migrated_provider
):
    query = f"Plan a 3-day trip to {city} for 1 traveler under $10000 total."
    baseline = TravelService().plan(query)
    service = TravelService(tool_runner=partial(run_tool, provider=migrated_provider))
    app.dependency_overrides[get_travel_service] = lambda: service
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/travel/plan", json={"query": query})
    finally:
        app.dependency_overrides.pop(get_travel_service, None)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["budget"] == baseline.budget.model_dump(mode="json")
    assert body["budget"]["estimated_total_cost"] == expected_total
    assert body["execution"]["validation"] == baseline.execution.validation.model_dump(mode="json")
    assert body["execution"]["replan_attempts"] == baseline.execution.replan_attempts == 0
    assert [tool["source"] for tool in body["execution"]["tools"][:4]] == [
        "snapshot",
        "snapshot",
        "snapshot",
        "mock",
    ]
    groups = {group["category"]: group for group in body["execution"]["candidate_groups"]}
    for category in ("attractions", "hotel", "food"):
        rows = groups[category]["selected"] + groups[category]["alternatives"]
        assert len(rows) == 3
        assert all(row["provider"] == "openstreetmap" for row in rows)
        assert all(row.get("rating") is None and row.get("review_count") is None for row in rows)
    transport = groups["transport"]["selected"] + groups["transport"]["alternatives"]
    assert all(row.get("provider") is None for row in transport)
