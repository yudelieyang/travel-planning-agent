import json

import pytest

from app.agent.service import PlanResponse, TravelService
from app.tools import candidate_data, mock
from app.tools.contracts import SearchInput, ToolResult, ToolStatus, TravelOption

SUPPORTED = {
    "Boston",
    "New York City",
    "Columbus",
    "Chicago",
    "Washington DC",
    "Miami",
    "Austin",
    "Denver",
    "Seattle",
    "San Francisco",
    "Los Angeles",
    "Las Vegas",
}
SEARCHES = [
    mock.search_attractions,
    mock.search_hotels,
    mock.search_restaurants,
    mock.search_transport,
]


def test_unified_dataset_covers_twelve_cities_and_every_category():
    dataset = candidate_data.load_candidate_dataset()
    assert dataset.source == "controlled_mock_fixture"
    assert {city.city for city in dataset.cities} == SUPPORTED
    assert sum(len(rows) for city in dataset.cities for rows in city.candidates.values()) == 150
    for city in dataset.cities:
        assert set(city.candidates) == {"attractions", "hotel", "food", "transport"}
        assert all(city.candidates.values())
        for search in SEARCHES:
            result = search(SearchInput(destination=city.city))
            assert result.status == ToolStatus.SUCCESS
            assert len(result.data) >= 3


def test_columbus_tools_match_zoo_and_fried_chicken_and_keep_alternatives():
    attractions = mock.search_attractions(
        SearchInput(destination="Columbus", preferences=["zoo"])
    )
    restaurants = mock.search_restaurants(
        SearchInput(destination="Columbus, OH", preferences=["fried chicken"])
    )
    hotels = mock.search_hotels(SearchInput(destination="Columbus Ohio"))
    transport = mock.search_transport(SearchInput(destination="Columbus"))
    assert all(
        result.status == ToolStatus.SUCCESS
        for result in (attractions, restaurants, hotels, transport)
    )
    assert len(attractions.data) == 5 and len(restaurants.data) == 6
    assert all("zoo" in row.tags for row in attractions.data[:3])
    assert all(row.preference_matches == ["zoo"] for row in attractions.data[:3])
    assert all("fried chicken" in row.tags for row in restaurants.data[:3])
    assert all(row.preference_matches == ["fried chicken"] for row in restaurants.data[:3])


def test_exact_soft_preference_matches_rank_before_fallback_candidates():
    result = mock.search_restaurants(
        SearchInput(destination="NYC", preferences=["seafood"])
    )

    assert result.status == ToolStatus.SUCCESS
    assert [row.id for row in result.data] == ["nyc-f3", "nyc-f1", "nyc-f2"]
    assert result.data[0].preference_matches == ["seafood"]
    assert all(row.preference_matches == [] for row in result.data[1:])


@pytest.mark.parametrize("search", SEARCHES)
def test_unmatched_soft_preference_returns_ranked_fallback_candidates(search):
    result = search(SearchInput(destination="NYC", preferences=["fried chicken"]))

    assert result.status == ToolStatus.SUCCESS
    assert len(result.data) == 3
    assert [row.price for row in result.data] == sorted(row.price for row in result.data)
    assert all(row.preference_matches == [] for row in result.data)


def test_hard_price_constraint_can_eliminate_candidates():
    result = mock.search_restaurants(
        SearchInput(destination="NYC", max_price=17, preferences=["fried chicken"])
    )

    assert result.status == ToolStatus.NO_RESULTS
    assert result.data == []


def test_genuinely_empty_eligible_pool_returns_no_results(monkeypatch):
    monkeypatch.setattr(mock, "candidates_for", lambda *args, **kwargs: [])

    result = mock.search_attractions(SearchInput(destination="Boston"))

    assert result.status == ToolStatus.NO_RESULTS
    assert result.error is None


def test_nyc_fried_chicken_falls_back_end_to_end():
    response = TravelService().plan(
        "Plan a 3-day trip to NYC. I like fried chicken."
    )

    assert response.status == "success"
    restaurant = next(
        tool for tool in response.execution.tools if tool.tool_name == "search_restaurants"
    )
    assert restaurant.status == ToolStatus.SUCCESS
    assert len(restaurant.data) == 3
    assert all(row.preference_matches == [] for row in restaurant.data)
    food = next(
        group for group in response.execution.candidate_groups if group.category == "food"
    )
    assert food.selected


def test_columbus_api_produces_full_itinerary_and_transparent_candidate_groups():
    response = TravelService().plan(
        "Plan a 3-day trip to Columbus. I like zoos and fried chicken."
    )
    assert response.status == "success"
    assert response.requirements.interests == ["zoo", "food"]
    assert response.requirements.food_preferences == ["fried chicken"]
    assert response.itinerary is not None and len(response.itinerary.daily_plan) == 3
    assert response.budget is not None
    assert all(tool.status == "SUCCESS" for tool in response.execution.tools)
    groups = {group.category: group for group in response.execution.candidate_groups}
    assert set(groups) == {"attractions", "hotel", "food", "transport"}
    assert all(group.selected for group in groups.values())
    assert all(2 <= len(group.alternatives) <= 3 for group in groups.values())
    for group in groups.values():
        assert not {row.id for row in group.selected} & {row.id for row in group.alternatives}
        for row in [*group.selected, *group.alternatives]:
            assert row.source == "controlled_mock_fixture"
            assert row.city == "Columbus" and row.state == "OH"
            assert row.price >= 0 and row.tags
            assert row.rating is None or 0 <= row.rating <= 5
            assert row.review_count is None or row.review_count >= 0
    assert PlanResponse.model_validate_json(response.model_dump_json()) == response


@pytest.mark.parametrize(
    "query,canonical",
    [
        ("Plan a 2-day trip to NYC.", "New York City"),
        ("Plan a 2-day trip to New York.", "New York City"),
        ("Plan a 2-day trip to New York City.", "New York City"),
        ("Plan a 2-day trip to Washington DC.", "Washington DC"),
        ("Plan a 2-day trip to Washington D.C.", "Washington DC"),
        ("Plan a 2-day trip to Washington, DC.", "Washington DC"),
        ("Plan a 2-day trip to Columbus, OH.", "Columbus"),
    ],
)
def test_city_aliases_use_the_fixture_registry(query, canonical):
    response = TravelService().plan(query)
    assert response.status == "success"
    assert response.requirements.destination == canonical
    assert {row.destination for group in response.execution.candidate_groups for row in group.selected} == {
        canonical
    }


@pytest.mark.parametrize("destination", ["Paris", "Tokyo", "Toronto", "Atlantis", "Nashville, TN"])
def test_unsupported_destinations_have_one_explicit_public_failure(destination):
    for search in SEARCHES:
        result = search(SearchInput(destination=destination))
        assert result.status == ToolStatus.NO_RESULTS
        assert result.error == "UNSUPPORTED_CITY_DATA"
    response = TravelService().plan(f"Plan a 2-day trip to {destination}.")
    assert response.status == "error"
    assert response.errors == ["UNSUPPORTED_CITY_DATA"]
    assert response.itinerary is response.budget is None
    assert response.execution.candidate_groups == []
    assert all(
        tool.error_code == "UNSUPPORTED_CITY_DATA" for tool in response.execution.tools[:4]
    )


def test_optional_candidate_metadata_round_trips_without_crashing():
    option = TravelOption(
        id="legacy-a1",
        destination="Legacy City",
        name="Legacy option",
        price=0,
        unit="per_person_visit",
        tags=[],
    )
    assert option.rating is option.review_count is option.image_url is option.source is None
    assert TravelOption.model_validate_json(option.model_dump_json()) == option
    transport = mock.search_transport(SearchInput(destination="Boston")).data[0]
    assert transport.rating is None and transport.review_count is None
    assert ToolResult.model_validate_json(
        mock.search_transport(SearchInput(destination="Boston")).model_dump_json()
    )


def test_city_can_be_added_by_fixture_data_only(monkeypatch, tmp_path):
    raw = json.loads(candidate_data.CANDIDATE_DATA_PATH.read_text(encoding="utf-8"))
    fixture_city = json.loads(json.dumps(raw["cities"][0]))
    fixture_city.update(city="Fixture City", state="FC", aliases=["Fixture City, FC"])
    for rows in fixture_city["candidates"].values():
        for row in rows:
            row["id"] = "fixture-" + row["id"]
    raw["cities"].append(fixture_city)
    path = tmp_path / "cities.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    monkeypatch.setattr(candidate_data, "CANDIDATE_DATA_PATH", path)
    candidate_data.load_candidate_dataset.cache_clear()
    try:
        assert mock.search_hotels(SearchInput(destination="Fixture City, FC")).status == "SUCCESS"
    finally:
        candidate_data.load_candidate_dataset.cache_clear()


@pytest.mark.parametrize("destination", ["Boston", "NYC"])
def test_existing_city_regressions_and_wave3_repair(destination):
    assert TravelService().plan(f"Plan a 3-day trip to {destination}.").status == "success"
    repaired = TravelService().plan(
        "Plan a 2-day trip to Boston for 2 travelers under $400 total."
    )
    assert repaired.status == "success"
    assert repaired.execution.replan_attempts == 1
    assert repaired.execution.validation.outcome == "passed"
    assert repaired.budget.estimated_total_cost <= 400
