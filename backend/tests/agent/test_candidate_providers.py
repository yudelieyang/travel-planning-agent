import copy
import json

import pytest

from app.core.config import PROJECT_ROOT, Settings
from app.tools.candidate_data import candidates_for
from app.tools.candidate_providers import (
    CandidateProviderError,
    MixedCandidateProvider,
    MockFixtureProvider,
    RealSnapshotProvider,
    create_candidate_provider,
)
from app.tools.contracts import SearchInput
from app.tools.mock import search_attractions, search_hotels, search_restaurants, search_transport

OSM_PILOT = PROJECT_ROOT / "data/travel/snapshots/openstreetmap/migration_manifest.json"
OSM_HOTELS = (
    PROJECT_ROOT
    / "data/travel/snapshots/openstreetmap/osm_boston_hotels_2026-09-16_v1/boston_hotels.json"
)
OSM_FOOD = (
    PROJECT_ROOT
    / "data/travel/snapshots/openstreetmap/osm_boston_food_2026-09-16_v1/boston_food.json"
)
OSM_AUSTIN_ATTRACTIONS = (
    PROJECT_ROOT
    / "data/travel/snapshots/openstreetmap/osm_austin_attractions_2026-09-16_v1/austin_attractions.json"
)
OSM_COLUMBUS = {
    "attractions": PROJECT_ROOT
    / "data/travel/snapshots/openstreetmap/osm_columbus_attractions_2026-09-16_v1/columbus_attractions.json",
    "hotel": PROJECT_ROOT
    / "data/travel/snapshots/openstreetmap/osm_columbus_hotels_2026-09-16_v1/columbus_hotels.json",
    "food": PROJECT_ROOT
    / "data/travel/snapshots/openstreetmap/osm_columbus_food_2026-09-16_v1/columbus_food.json",
}


def snapshot_data():
    return {
        "snapshot_version": "fsq_test_v1",
        "snapshot_fetched_at": "2026-09-16T12:00:00Z",
        "provider": "fsq_os_places",
        "source": "real_snapshot",
        "cities": [
            {
                "city": "Boston",
                "state": "MA",
                "candidates": {
                    "hotel": [
                        {
                            "id": "real-bos-h1",
                            "provider_place_id": "fsq-1",
                            "name": "Example Harbor Hotel",
                            "address": "1 Test Street",
                            "latitude": 42.36,
                            "longitude": -71.06,
                            "provider_category_ids": ["hotel-category"],
                            "provider_category_labels": ["Travel and Transportation > Hotel"],
                            "provider_refreshed_at": "2026-09-15T00:00:00Z",
                            "price": 100,
                            "currency": "USD",
                            "unit": "per_person_night",
                            "tags": ["central"],
                            "cost_origin": "planner_estimate",
                            "cost_method": "controlled_demo_estimate",
                            "cost_version": "v1",
                        },
                        {
                            "id": "real-bos-h2",
                            "provider_place_id": "fsq-2",
                            "name": "Example Garden Hotel",
                            "latitude": 42.35,
                            "longitude": -71.07,
                            "provider_category_ids": ["hotel-category"],
                            "price": 130,
                            "currency": "USD",
                            "unit": "per_person_night",
                            "tags": ["quiet"],
                            "cost_origin": "planner_estimate",
                            "cost_method": "controlled_demo_estimate",
                            "cost_version": "v1",
                        },
                    ]
                },
            }
        ],
    }


def write_snapshot(tmp_path, data=None):
    path = tmp_path / "snapshot.json"
    path.write_text(json.dumps(snapshot_data() if data is None else data), encoding="utf-8")
    return path


def test_mock_provider_matches_compatibility_facade_and_preserves_serialized_shape():
    expected = candidates_for("NYC", "food", max_price=25, preferences=["vegetarian"])
    actual = candidates_for(
        "NYC",
        "food",
        max_price=25,
        preferences=["vegetarian"],
        provider=MockFixtureProvider(),
    )

    assert actual == expected
    assert [row.id for row in actual] == ["nyc-f1", "nyc-f2"]
    dumped = actual[0].model_dump()
    assert "provider" not in dumped and "snapshot_version" not in dumped


def test_real_snapshot_provider_loads_and_uses_existing_filter_and_ranking(tmp_path):
    provider = RealSnapshotProvider(write_snapshot(tmp_path))

    options = candidates_for("Boston, MA", "hotel", preferences=["quiet"], provider=provider)

    assert [row.id for row in options] == ["real-bos-h2", "real-bos-h1"]
    assert options[0].source == "real_snapshot"
    assert options[0].provider == "fsq_os_places"
    assert options[0].snapshot_version == "fsq_test_v1"
    assert options[0].cost_origin == "planner_estimate"
    assert options[0].preference_matches == ["quiet"]
    assert candidates_for("Boston", "hotel", max_price=99, provider=provider) == []
    assert candidates_for("Boston", "food", provider=provider) == []
    assert provider.candidates("Atlantis", "hotel") is None
    result = search_hotels(SearchInput(destination="Boston"), provider)
    assert result.source == "snapshot" and result.data[0].provider == "fsq_os_places"


def test_mode_selection_defaults_to_mock_and_requires_an_explicit_snapshot(tmp_path):
    assert isinstance(create_candidate_provider("mock"), MockFixtureProvider)
    assert isinstance(create_candidate_provider("snapshot", OSM_PILOT), MixedCandidateProvider)
    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot")


def test_candidate_settings_default_to_mock_and_resolve_snapshot_paths():
    default = Settings(
        _env_file=None,
        postgres_db="test",
        postgres_user="test",
        postgres_password="test",
    )
    snapshot = Settings(
        _env_file=None,
        postgres_db="test",
        postgres_user="test",
        postgres_password="test",
        candidate_data_mode="snapshot",
        candidate_snapshot_path="data/travel/snapshots/test.json",
    )

    assert default.candidate_data_mode == "mock" and default.candidate_snapshot_path is None
    assert (
        snapshot.candidate_snapshot_path
        == (PROJECT_ROOT / "data/travel/snapshots/test.json").resolve()
    )


@pytest.mark.parametrize(
    "mutate",
    [
        lambda data: data["cities"][0]["candidates"]["hotel"].append(
            {
                **copy.deepcopy(data["cities"][0]["candidates"]["hotel"][0]),
                "provider_place_id": "fsq-duplicate-internal-id",
            }
        ),
        lambda data: data["cities"][0]["candidates"]["hotel"].append(
            {
                **copy.deepcopy(data["cities"][0]["candidates"]["hotel"][0]),
                "id": "real-bos-h3",
            }
        ),
        lambda data: data["cities"][0]["candidates"]["hotel"][0].update(latitude=91),
        lambda data: data["cities"][0]["candidates"]["hotel"][0].pop("longitude"),
        lambda data: data.pop("provider"),
        lambda data: data.update(snapshot_fetched_at="2026-09-16T12:00:00"),
        lambda data: data["cities"][0]["candidates"]["hotel"][0].update(
            provider_refreshed_at="2026-09-15T00:00:00"
        ),
        lambda data: data.update(snapshot_version="INVALID VERSION"),
        lambda data: data["cities"][0]["candidates"]["hotel"][0].update(
            cost_origin="provider_observed"
        ),
        lambda data: data["cities"][0]["candidates"]["hotel"][0].update(unit="per_person_meal"),
        lambda data: data["cities"][0]["candidates"]["hotel"][0].update(price=-1),
        lambda data: data["cities"][0].update(city="Paris", state="FR"),
        lambda data: data["cities"][0]["candidates"]["hotel"][0].update(name=""),
        lambda data: data["cities"][0].update(candidates={"unsupported": []}),
    ],
)
def test_invalid_snapshots_fail_closed_without_mock_fallback(tmp_path, mutate):
    data = snapshot_data()
    mutate(data)

    with pytest.raises(CandidateProviderError):
        RealSnapshotProvider(write_snapshot(tmp_path, data))


def test_malformed_json_fails_closed_without_mock_fallback(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{not-json", encoding="utf-8")

    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", path)


def test_osm_pilot_routes_migrated_boston_categories_to_snapshot():
    provider = create_candidate_provider("snapshot", OSM_PILOT)
    attractions = search_attractions(SearchInput(destination="Boston, MA"), provider)
    hotels = search_hotels(SearchInput(destination="Boston"), provider)
    food = search_restaurants(SearchInput(destination="Boston"), provider)

    assert attractions.source == "snapshot"
    assert [row.id for row in attractions.data] == ["bos-a3", "bos-a2", "bos-a1"]
    assert [row.price for row in sorted(attractions.data, key=lambda row: row.id)] == [20, 15, 0]
    assert {row.provider for row in attractions.data} == {"openstreetmap"}
    assert all(
        row.provider_place_id.startswith(("node/", "way/", "relation/")) for row in attractions.data
    )
    assert all(
        row.address and row.latitude is not None and row.longitude is not None
        for row in attractions.data
    )
    assert all(row.cost_origin == "planner_estimate" for row in attractions.data)
    assert all(
        row.cost_method == "legacy_demo_cost_preserved_for_phase_o_migration"
        for row in attractions.data
    )
    assert all(row.cost_version == "phase_o_v1" for row in attractions.data)
    assert all(row.rating is None and row.review_count is None for row in attractions.data)
    assert {
        row.id: (row.provider_category_ids, row.provider_category_labels, row.tags)
        for row in attractions.data
    } == {
        "bos-a1": (["tourism=museum"], ["Museum"], ["museums"]),
        "bos-a2": (["tourism=aquarium"], ["Aquarium"], ["aquarium"]),
        "bos-a3": (["leisure=park"], ["Park"], ["parks"]),
    }

    assert hotels.source == "snapshot"
    assert [row.id for row in hotels.data] == ["bos-h1", "bos-h2", "bos-h3"]
    assert [row.name for row in hotels.data] == [
        "Boston Harbor Hotel",
        "The Eliot Hotel",
        "Four Seasons Hotel Boston",
    ]
    assert [row.price for row in hotels.data] == [100, 130, 220]
    assert all(row.unit == "per_person_night" for row in hotels.data)
    assert all(row.provider == "openstreetmap" for row in hotels.data)
    assert all(
        row.provider_place_id.startswith(("node/", "way/", "relation/")) for row in hotels.data
    )
    assert all(
        row.address and row.latitude is not None and row.longitude is not None
        for row in hotels.data
    )
    assert all(row.cost_origin == "planner_estimate" for row in hotels.data)
    assert all(
        row.cost_method == "legacy_demo_cost_preserved_for_phase_o_migration" for row in hotels.data
    )
    assert all(row.cost_version == "phase_o_v1" for row in hotels.data)
    assert all(row.rating is None and row.review_count is None for row in hotels.data)
    assert all(row.provider_category_ids == ["tourism=hotel"] for row in hotels.data)

    assert food.source == "snapshot"
    assert [row.id for row in food.data] == ["bos-f1", "bos-f2", "bos-f3"]
    assert [row.name for row in food.data] == [
        "Aceituna Grill",
        "India Quality",
        "Atlantic Fish",
    ]
    assert [row.price for row in food.data] == [16, 20, 30]
    assert all(row.unit == "per_person_meal" for row in food.data)
    assert all(row.provider == "openstreetmap" for row in food.data)
    assert all(
        row.provider_place_id.startswith(("node/", "way/", "relation/")) for row in food.data
    )
    assert all(
        row.address and row.latitude is not None and row.longitude is not None for row in food.data
    )
    assert all(row.cost_origin == "planner_estimate" for row in food.data)
    assert all(
        row.cost_method == "legacy_demo_cost_preserved_for_phase_o_migration" for row in food.data
    )
    assert all(row.cost_version == "phase_o_v1" for row in food.data)
    assert all(row.rating is None and row.review_count is None for row in food.data)
    assert {
        row.id: (row.provider_category_ids, row.provider_category_labels, row.tags)
        for row in food.data
    } == {
        "bos-f1": (
            [
                "amenity=restaurant",
                "cuisine=mediterranean",
                "diet:vegetarian=yes",
                "diet:vegan=yes",
            ],
            [
                "Restaurant",
                "Cuisine: Mediterranean",
                "Vegetarian options",
                "Vegan options",
            ],
            ["vegetarian", "vegan"],
        ),
        "bos-f2": (
            [
                "amenity=restaurant",
                "cuisine=indian",
                "diet:vegetarian=yes",
                "diet:vegan=yes",
            ],
            [
                "Restaurant",
                "Cuisine: Indian",
                "Vegetarian options",
                "Vegan options",
            ],
            ["vegetarian"],
        ),
        "bos-f3": (
            ["amenity=restaurant", "cuisine=seafood"],
            ["Restaurant", "Cuisine: Seafood"],
            ["seafood"],
        ),
    }

    mock_provider = MockFixtureProvider()
    for max_price, preferences in ((129, []), (None, ["quiet"]), (220, ["central"])):
        real = candidates_for(
            "Boston", "hotel", max_price=max_price, preferences=preferences, provider=provider
        )
        mock = candidates_for(
            "Boston", "hotel", max_price=max_price, preferences=preferences, provider=mock_provider
        )
        assert [row.id for row in real] == [row.id for row in mock]

    for max_price, preferences in (
        (19, []),
        (None, ["vegetarian"]),
        (None, ["seafood"]),
    ):
        real = candidates_for(
            "Boston", "food", max_price=max_price, preferences=preferences, provider=provider
        )
        mock = candidates_for(
            "Boston",
            "food",
            max_price=max_price,
            preferences=preferences,
            provider=MockFixtureProvider(),
        )
        assert [row.id for row in real] == [row.id for row in mock]

    transport = search_transport(SearchInput(destination="Boston"), provider)
    assert transport.source == "mock"
    assert all(
        row.source == "controlled_mock_fixture" and row.provider is None for row in transport.data
    )


def test_austin_manifest_routes_pois_to_snapshot_and_transport_to_mock():
    provider = create_candidate_provider("snapshot", OSM_PILOT)
    results = {
        "attractions": search_attractions(SearchInput(destination="Austin, TX"), provider),
        "hotel": search_hotels(SearchInput(destination="Austin"), provider),
        "food": search_restaurants(SearchInput(destination="Austin"), provider),
    }

    assert {category: result.source for category, result in results.items()} == {
        "attractions": "snapshot",
        "hotel": "snapshot",
        "food": "snapshot",
    }
    assert {
        category: [(row.id, row.name, row.price, row.unit, row.tags) for row in result.data]
        for category, result in results.items()
    } == {
        "attractions": [
            ("aus-a3", "Zilker Park", 5, "per_person_visit", ["parks", "outdoors"]),
            (
                "aus-a2",
                "Texas Music Museum",
                17,
                "per_person_visit",
                ["museums", "history", "music"],
            ),
            (
                "aus-a1",
                "Blanton Museum of Art",
                19,
                "per_person_visit",
                ["museums", "art"],
            ),
        ],
        "hotel": [
            ("aus-h1", "Hilton Austin", 88, "per_person_night", ["budget", "central"]),
            ("aus-h2", "Hyatt Regency Austin", 120, "per_person_night", ["quiet"]),
            (
                "aus-h3",
                "Four Seasons Hotel Austin",
                205,
                "per_person_night",
                ["luxury", "central"],
            ),
        ],
        "food": [
            ("aus-f1", "Veracruz All Natural", 14, "per_person_meal", ["tacos", "local"]),
            (
                "aus-f2",
                "Bouldin Creek Cafe",
                18,
                "per_person_meal",
                ["vegetarian", "vegan"],
            ),
            ("aus-f3", "Franklin Barbecue", 27, "per_person_meal", ["barbecue", "local"]),
        ],
    }
    rows = [row for result in results.values() for row in result.data]
    assert len(rows) == 9
    assert all(row.provider == "openstreetmap" for row in rows)
    assert all(row.provider_place_id.startswith(("node/", "way/", "relation/")) for row in rows)
    assert all(
        row.address and row.latitude is not None and row.longitude is not None for row in rows
    )
    assert all(row.source == "real_snapshot" and row.snapshot_version for row in rows)
    assert all(row.cost_origin == "planner_estimate" for row in rows)
    assert all(
        row.cost_method == "legacy_demo_cost_preserved_for_phase_o_migration" for row in rows
    )
    assert all(row.cost_version == "phase_o_v1" for row in rows)
    assert all(row.rating is None and row.review_count is None for row in rows)
    assert {
        row.id: (row.provider_place_id, row.address, row.latitude, row.longitude) for row in rows
    } == {
        "aus-a1": (
            "relation/20972967",
            "200 East Martin Luther King Jr Boulevard, Austin, TX 78705",
            30.2809842,
            -97.7374171,
        ),
        "aus-a2": (
            "way/379207889",
            "1011 San Marcos Street, TX",
            30.2694425,
            -97.7306205,
        ),
        "aus-a3": (
            "way/946120954",
            "Barton Springs Road, AUSTIN, TX 78746",
            30.2676819,
            -97.7666085,
        ),
        "aus-h1": (
            "node/12577833089",
            "500 East 4th Street, Austin, TX 78701",
            30.2652582,
            -97.73806,
        ),
        "aus-h2": (
            "way/104137285",
            "208 Barton Springs Road, Austin, TX 78704",
            30.2607066,
            -97.7467623,
        ),
        "aus-h3": (
            "way/134807221",
            "98 San Jacinto Blvd, Austin, TX 78701",
            30.2616262,
            -97.7422786,
        ),
        "aus-f1": (
            "way/802335915",
            "2505 Webberville Road, Austin, TX 78702",
            30.2630626,
            -97.7137458,
        ),
        "aus-f2": (
            "way/382491308",
            "1900 South 1st Street, Austin, TX 78704",
            30.2464901,
            -97.7568002,
        ),
        "aus-f3": (
            "way/382368408",
            "900 East 11th Street, Austin, TX 78702",
            30.2701634,
            -97.7312704,
        ),
    }
    assert {row.snapshot_version for row in rows} == {
        "osm_austin_attractions_2026-09-16_v1",
        "osm_austin_hotels_2026-09-16_v1",
        "osm_austin_food_2026-09-16_v1",
    }
    assert results["food"].data[0].provider_category_ids == [
        "amenity=restaurant",
        "cuisine=mexican",
    ]
    assert results["food"].data[1].provider_category_ids == [
        "amenity=restaurant",
        "diet:vegetarian=only",
        "diet:vegan=yes",
    ]
    assert results["food"].data[2].provider_category_ids == [
        "amenity=restaurant",
        "cuisine=barbecue",
    ]

    mock = MockFixtureProvider()
    for category, max_price, preferences in (
        ("attractions", 17, ["parks"]),
        ("hotel", 120, ["quiet"]),
        ("food", 18, ["vegetarian"]),
    ):
        real_rows = candidates_for(
            "Austin", category, max_price=max_price, preferences=preferences, provider=provider
        )
        mock_rows = candidates_for(
            "Austin", category, max_price=max_price, preferences=preferences, provider=mock
        )
        assert [row.id for row in real_rows] == [row.id for row in mock_rows]

    transport = search_transport(SearchInput(destination="Austin"), provider)
    assert transport.source == "mock"
    assert [row.id for row in transport.data] == ["aus-t1", "aus-t2", "aus-t3"]
    assert all(
        row.provider is None and row.source == "controlled_mock_fixture" for row in transport.data
    )


def test_columbus_manifest_preserves_real_facts_costs_and_preference_contracts():
    provider = create_candidate_provider("snapshot", OSM_PILOT)
    results = {
        "attractions": search_attractions(
            SearchInput(destination="Columbus, OH", preferences=["zoo"]), provider
        ),
        "hotel": search_hotels(SearchInput(destination="Columbus", max_price=200), provider),
        "food": search_restaurants(
            SearchInput(destination="Columbus", preferences=["fried chicken"]), provider
        ),
    }

    assert {category: result.source for category, result in results.items()} == {
        "attractions": "snapshot",
        "hotel": "snapshot",
        "food": "snapshot",
    }
    assert {
        category: [(row.id, row.name, row.price, row.unit, row.tags) for row in result.data]
        for category, result in results.items()
    } == {
        "attractions": [
            (
                "cmh-a5",
                "Scioto Audubon Metro Park",
                0,
                "per_person_visit",
                ["zoo", "parks", "walking"],
            ),
            ("cmh-a3", "Ohio History Center", 18, "per_person_visit", ["zoo", "animals", "family"]),
            (
                "cmh-a4",
                "National Veterans Memorial and Museum",
                20,
                "per_person_visit",
                ["zoo", "science", "museums"],
            ),
            ("cmh-a1", "COSI", 22, "per_person_visit", ["zoo", "animals", "family"]),
            (
                "cmh-a2",
                "Columbus Museum of Art",
                28,
                "per_person_visit",
                ["zoo", "animals", "outdoors"],
            ),
        ],
        "hotel": [
            (
                "cmh-h1",
                "Days Inn by Wyndham Columbus Fairgrounds",
                82,
                "per_person_night",
                ["budget", "central"],
            ),
            ("cmh-h2", "Holiday Inn Express", 105, "per_person_night", ["quiet", "neighborhood"]),
            (
                "cmh-h3",
                "Hampton Inn & Suites Columbus Downtown",
                135,
                "per_person_night",
                ["central"],
            ),
            (
                "cmh-h4",
                "The Westin Great Southern Columbus",
                190,
                "per_person_night",
                ["luxury", "quiet"],
            ),
        ],
        "food": [
            (
                "cmh-f1",
                "Jerky's Jamaican Grill",
                14,
                "per_person_meal",
                ["fried chicken", "comfort food"],
            ),
            ("cmh-f6", "BonChon Chicken", 16, "per_person_meal", ["fried chicken", "casual"]),
            (
                "cmh-f2",
                "Feed Me! Sandwich Kings!",
                17,
                "per_person_meal",
                ["fried chicken", "market"],
            ),
            ("cmh-f4", "CM Chicken", 18, "per_person_meal", ["fried chicken", "casual"]),
            ("cmh-f3", "The Crispy Coop", 20, "per_person_meal", ["fried chicken", "casual"]),
            ("cmh-f5", "OX-B's", 26, "per_person_meal", ["fried chicken", "local"]),
        ],
    }
    rows = [row for result in results.values() for row in result.data]
    assert all(row.provider == "openstreetmap" and row.source == "real_snapshot" for row in rows)
    assert all(
        row.address and row.latitude is not None and row.longitude is not None for row in rows
    )
    assert all(
        row.cost_origin == "planner_estimate" and row.cost_version == "phase_o_v1" for row in rows
    )
    assert all(row.rating is None and row.review_count is None for row in rows)
    assert all(row.preference_matches == ["zoo"] for row in results["attractions"].data)
    assert all(row.preference_matches == ["fried chicken"] for row in results["food"].data)

    identities = {row.id: row.provider_place_id for row in rows}
    assert identities == {
        "cmh-a1": "way/32873150",
        "cmh-a2": "way/293476179",
        "cmh-a3": "way/835107792",
        "cmh-a4": "way/570391114",
        "cmh-a5": "way/224492486",
        "cmh-h1": "way/717324868",
        "cmh-h2": "way/474605329",
        "cmh-h3": "node/4685223268",
        "cmh-h4": "node/1376126720",
        "cmh-f1": "node/8343623182",
        "cmh-f2": "node/8481484417",
        "cmh-f3": "node/8561182617",
        "cmh-f4": "node/9993723530",
        "cmh-f5": "node/14093010165",
        "cmh-f6": "way/512159964",
    }
    provider_facts = {row.id: row.provider_category_ids for row in results["food"].data}
    assert "cuisine=fried_chicken" in provider_facts["cmh-f1"]
    assert all(
        "cuisine=fried_chicken" not in provider_facts[candidate_id]
        for candidate_id in ("cmh-f2", "cmh-f3", "cmh-f4", "cmh-f5", "cmh-f6")
    )
    assert all("fried chicken" not in fact for facts in provider_facts.values() for fact in facts)

    mock = MockFixtureProvider()
    for category, max_price, preferences in (
        ("attractions", None, ["zoo"]),
        ("hotel", 200, []),
        ("food", None, ["fried chicken"]),
    ):
        real_rows = candidates_for(
            "Columbus", category, max_price=max_price, preferences=preferences, provider=provider
        )
        mock_rows = candidates_for(
            "Columbus", category, max_price=max_price, preferences=preferences, provider=mock
        )
        assert [row.id for row in real_rows] == [row.id for row in mock_rows]

    transport = search_transport(SearchInput(destination="Columbus"), provider)
    assert transport.source == "mock"
    assert [row.id for row in transport.data] == ["cmh-t1", "cmh-t2", "cmh-t3"]
    assert all(
        row.provider is None and row.source == "controlled_mock_fixture" for row in transport.data
    )


@pytest.mark.parametrize("category", ["attractions", "hotel", "food"])
@pytest.mark.parametrize("failure", ["missing", "corrupt", "empty", "wrong_city", "wrong_category"])
def test_declared_columbus_routes_fail_closed(tmp_path, category, failure):
    snapshot_path = tmp_path / "snapshot.json"
    route = {"city": "Columbus", "category": category, "snapshot": "snapshot.json"}
    if failure == "corrupt":
        snapshot_path.write_text("{not-json", encoding="utf-8")
    elif failure != "missing":
        snapshot = json.loads(OSM_COLUMBUS[category].read_text(encoding="utf-8"))
        if failure == "empty":
            snapshot["cities"][0]["candidates"][category] = []
        elif failure == "wrong_city":
            route["city"] = "Boston"
        elif failure == "wrong_category":
            route["category"] = "transport"
        snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps({"manifest_version": "test_v1", "routes": [route]}), encoding="utf-8"
    )

    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", manifest_path)


@pytest.mark.parametrize("failure", ["missing", "corrupt", "empty", "wrong_city", "wrong_category"])
def test_declared_austin_route_failures_never_fall_back_to_mock(tmp_path, failure):
    snapshot_path = tmp_path / "attractions.json"
    route = {"city": "Austin", "category": "attractions", "snapshot": "attractions.json"}
    if failure == "corrupt":
        snapshot_path.write_text("{not-json", encoding="utf-8")
    elif failure != "missing":
        snapshot = json.loads(OSM_AUSTIN_ATTRACTIONS.read_text(encoding="utf-8"))
        if failure == "empty":
            snapshot["cities"][0]["candidates"]["attractions"] = []
        elif failure == "wrong_city":
            route["city"] = "Boston"
        elif failure == "wrong_category":
            route["category"] = "hotel"
        snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps({"manifest_version": "test_v1", "routes": [route]}), encoding="utf-8"
    )

    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", manifest_path)


def test_declared_migration_routes_fail_closed_without_mock_fallback(tmp_path):
    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", tmp_path / "missing.json")

    manifest = {
        "manifest_version": "test_v1",
        "routes": [{"city": "Boston", "category": "hotel", "snapshot": "hotel.json"}],
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", manifest_path)

    (tmp_path / "hotel.json").write_text("{not-json", encoding="utf-8")
    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", manifest_path)

    hotel = json.loads(OSM_HOTELS.read_text(encoding="utf-8"))
    hotel["cities"][0]["candidates"]["hotel"] = []
    (tmp_path / "hotel.json").write_text(json.dumps(hotel), encoding="utf-8")
    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", manifest_path)


def test_declared_food_route_missing_corrupt_or_empty_fails_closed(tmp_path):
    manifest = {
        "manifest_version": "test_v1",
        "routes": [{"city": "Boston", "category": "food", "snapshot": "food.json"}],
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", manifest_path)

    food_path = tmp_path / "food.json"
    food_path.write_text("{not-json", encoding="utf-8")
    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", manifest_path)

    food = json.loads(OSM_FOOD.read_text(encoding="utf-8"))
    food["cities"][0]["candidates"]["food"] = []
    food_path.write_text(json.dumps(food), encoding="utf-8")
    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", manifest_path)


def test_osm_food_missing_cuisine_is_omitted_without_invention(tmp_path):
    food = json.loads(OSM_FOOD.read_text(encoding="utf-8"))
    row = food["cities"][0]["candidates"]["food"][0]
    row["provider_category_ids"] = ["amenity=restaurant"]
    row["provider_category_labels"] = ["Restaurant"]
    path = tmp_path / "food.json"
    path.write_text(json.dumps(food), encoding="utf-8")

    candidate = RealSnapshotProvider(path).candidates("Boston", "food")[0]

    assert candidate.provider_category_ids == ["amenity=restaurant"]
    assert candidate.provider_category_labels == ["Restaurant"]
    assert not any(value.startswith("cuisine=") for value in candidate.provider_category_ids)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda data: data["cities"][0]["candidates"]["food"][0].update(
            provider_place_id="12663666560"
        ),
        lambda data: data["cities"][0]["candidates"]["food"][0].update(latitude=91),
        lambda data: data["cities"][0]["candidates"]["food"].append(
            {
                **copy.deepcopy(data["cities"][0]["candidates"]["food"][0]),
                "id": "bos-f4",
            }
        ),
        lambda data: data["cities"][0].update(city="New York City", state="NY"),
    ],
)
def test_invalid_osm_food_identity_location_or_city_fails_closed(tmp_path, mutation):
    food = json.loads(OSM_FOOD.read_text(encoding="utf-8"))
    mutation(food)
    food_path = tmp_path / "food.json"
    food_path.write_text(json.dumps(food), encoding="utf-8")
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "manifest_version": "test_v1",
                "routes": [{"city": "Boston", "category": "food", "snapshot": "food.json"}],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", manifest_path)


def test_food_manifest_route_with_wrong_category_fails_closed(tmp_path):
    (tmp_path / "food.json").write_text(OSM_FOOD.read_text(encoding="utf-8"), encoding="utf-8")
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "manifest_version": "test_v1",
                "routes": [{"city": "Boston", "category": "hotel", "snapshot": "food.json"}],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", manifest_path)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda row: row.update(provider_place_id="1325873780"),
        lambda row: row.update(provider_place_id="way/not-a-number"),
        lambda row: row.update(latitude=91),
    ],
)
def test_invalid_osm_hotel_identity_or_coordinates_fail_closed(tmp_path, mutation):
    hotel = json.loads(OSM_HOTELS.read_text(encoding="utf-8"))
    mutation(hotel["cities"][0]["candidates"]["hotel"][0])
    snapshot_path = tmp_path / "hotel.json"
    snapshot_path.write_text(json.dumps(hotel), encoding="utf-8")
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "manifest_version": "test_v1",
                "routes": [{"city": "Boston", "category": "hotel", "snapshot": "hotel.json"}],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(CandidateProviderError):
        create_candidate_provider("snapshot", manifest_path)


def test_osm_stars_remain_provider_metadata_and_never_become_rating(tmp_path):
    hotel = json.loads(OSM_HOTELS.read_text(encoding="utf-8"))
    row = hotel["cities"][0]["candidates"]["hotel"][0]
    row["provider_category_ids"].append("stars=5")
    row["provider_category_labels"].append("5-star classification")
    path = tmp_path / "hotel.json"
    path.write_text(json.dumps(hotel), encoding="utf-8")

    candidate = RealSnapshotProvider(path).candidates("Boston", "hotel")[0]

    assert candidate.rating is None and candidate.review_count is None
    assert "stars=5" in candidate.provider_category_ids
