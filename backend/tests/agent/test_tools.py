import pytest
from pydantic import ValidationError

from app.tools import mock
from app.tools.contracts import BudgetInput, CostItem, SearchInput, ToolResult, ToolStatus


@pytest.mark.parametrize(
    "function",
    [mock.search_attractions, mock.search_hotels, mock.search_restaurants, mock.search_transport],
)
def test_search_contract_and_no_results(function):
    result = function(SearchInput(destination="Boston"))
    assert result.status == ToolStatus.SUCCESS
    assert result.source == "mock"
    assert len(result.data) == 3
    assert ToolResult.model_validate_json(result.model_dump_json()) == result
    assert function(SearchInput(destination="Atlantis")).status == ToolStatus.NO_RESULTS


def test_search_filters_and_validation():
    result = mock.search_hotels(
        SearchInput(destination="NYC", max_price=130, preferences=["budget"])
    )
    assert [row.id for row in result.data] == ["nyc-h1"]
    assert (
        mock.search_hotels(SearchInput(destination="Boston", max_price=1)).status
        == ToolStatus.NO_RESULTS
    )
    with pytest.raises(ValidationError):
        SearchInput(destination="Boston", max_price=-1)


def test_fixture_failure_returns_error(monkeypatch, tmp_path):
    monkeypatch.setattr(mock, "MOCK_ROOT", tmp_path)
    result = mock.search_hotels(SearchInput(destination="Boston"))
    assert result.status == ToolStatus.ERROR
    assert result.error
    assert result.data is None


def test_budget_decimal_arithmetic_and_group_size():
    request = BudgetInput(
        items=[CostItem(category="food", amount=0.1), CostItem(category="hotel", amount=0.2)],
        travelers=2,
        limit=0.6,
        budget_scope="TOTAL_TRIP",
    )
    result = mock.calculate_budget(request)
    assert result.source == "deterministic"
    assert result.data.per_traveler_cost == 0.3
    assert result.data.estimated_total_cost == 0.6
    assert result.data.breakdown["hotel"] == 0.4
    assert result.data.breakdown["food"] == 0.2
    assert result.data.within_budget is True


def test_budget_unknown_party_and_currency_are_not_fabricated():
    unknown = mock.calculate_budget(
        BudgetInput(
            items=[CostItem(category="food", amount=20)], limit=10, budget_scope="TOTAL_TRIP"
        )
    ).data
    assert unknown.basis == "per_traveler"
    assert unknown.travelers is None
    assert unknown.within_budget is None
    assert any("exceeds" in warning for warning in unknown.warnings)
    foreign = mock.calculate_budget(
        BudgetInput(items=[], travelers=1, limit=100, limit_currency="EUR")
    ).data
    assert foreign.within_budget is None
    assert any("currency" in warning for warning in foreign.warnings)


@pytest.mark.parametrize(
    "values",
    [
        {"status": "ERROR"},
        {"status": "SUCCESS"},
        {"status": "NO_RESULTS", "error": "invalid"},
    ],
)
def test_result_contract_rejects_inconsistent_status(values):
    with pytest.raises(ValidationError):
        ToolResult(tool_name="test", source="mock", **values)
