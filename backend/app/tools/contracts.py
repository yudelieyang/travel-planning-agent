"""Typed, source-independent tool requests and results."""

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.budget import BudgetScope

Category = Literal["attractions", "hotel", "food", "transport"]
SearchToolName = Literal[
    "search_attractions", "search_hotels", "search_restaurants", "search_transport"
]


class ToolModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class SearchInput(ToolModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)
    destination: str = Field(min_length=1, max_length=100)
    max_price: float | None = Field(default=None, ge=0)
    preferences: list[str] = Field(default_factory=list)

    @field_validator("destination")
    @classmethod
    def nonblank_destination(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Destination cannot be blank")
        return value.strip()


class TravelOption(ToolModel):
    id: str
    destination: str
    city: str | None = None
    state: str | None = Field(default=None, min_length=2, max_length=2)
    category: Category | None = None
    name: str
    price: float = Field(ge=0)
    currency: Literal["USD"] = "USD"
    unit: Literal["per_person_visit", "per_person_night", "per_person_meal", "per_person_day"]
    tags: list[str]
    rating: float | None = Field(default=None, ge=0, le=5)
    review_count: int | None = Field(default=None, ge=0)
    image_url: str | None = None
    source: Literal["controlled_mock_fixture", "real_snapshot"] | None = None
    description: str | None = None
    preference_matches: list[str] = Field(default_factory=list)
    address: str | None = Field(default=None, exclude_if=lambda value: value is None)
    latitude: float | None = Field(default=None, ge=-90, le=90, exclude_if=lambda value: value is None)
    longitude: float | None = Field(
        default=None, ge=-180, le=180, exclude_if=lambda value: value is None
    )
    provider: str | None = Field(default=None, exclude_if=lambda value: value is None)
    provider_place_id: str | None = Field(default=None, exclude_if=lambda value: value is None)
    provider_category_ids: list[str] | None = Field(
        default=None, exclude_if=lambda value: value is None
    )
    provider_category_labels: list[str] | None = Field(
        default=None, exclude_if=lambda value: value is None
    )
    provider_refreshed_at: datetime | None = Field(
        default=None, exclude_if=lambda value: value is None
    )
    snapshot_version: str | None = Field(default=None, exclude_if=lambda value: value is None)
    snapshot_fetched_at: datetime | None = Field(
        default=None, exclude_if=lambda value: value is None
    )
    cost_origin: Literal["planner_estimate"] | None = Field(
        default=None, exclude_if=lambda value: value is None
    )
    cost_method: str | None = Field(default=None, exclude_if=lambda value: value is None)
    cost_version: str | None = Field(default=None, exclude_if=lambda value: value is None)

    @model_validator(mode="after")
    def validate_real_provenance(self):
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("Latitude and longitude must be supplied together")
        if self.source == "real_snapshot" and any(
            value is None
            for value in (
                self.provider,
                self.provider_place_id,
                self.snapshot_version,
                self.snapshot_fetched_at,
                self.cost_origin,
                self.cost_method,
                self.cost_version,
            )
        ):
            raise ValueError("Real snapshot candidates require provider, snapshot, and cost provenance")
        return self


class CostItem(ToolModel):
    category: Category
    amount: float = Field(ge=0)


class BudgetInput(ToolModel):
    items: list[CostItem]
    travelers: int | None = Field(default=None, ge=1, le=20)
    limit: float | None = Field(default=None, ge=0)
    limit_currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    budget_scope: BudgetScope = BudgetScope.UNKNOWN


class BudgetSummary(ToolModel):
    currency: Literal["USD"] = "USD"
    basis: Literal["group", "per_traveler"]
    travelers: int | None
    per_traveler_cost: float
    estimated_total_cost: float
    breakdown: dict[Category, float]
    provided_limit: float | None
    limit_currency: str
    budget_scope: BudgetScope = BudgetScope.UNKNOWN
    within_budget: bool | None
    comparison_cost: float | None = None
    remaining_budget: float | None = None
    warnings: list[str]


class ToolStatus(StrEnum):
    SUCCESS = "SUCCESS"
    NO_RESULTS = "NO_RESULTS"
    ERROR = "ERROR"


class ToolResult(ToolModel):
    tool_name: str
    status: ToolStatus
    data: list[TravelOption] | BudgetSummary | None = None
    source: str
    error: str | None = None
    metadata: dict[str, str | int] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_status(self):
        if self.status == ToolStatus.ERROR:
            if not self.error or self.data is not None:
                raise ValueError("ERROR requires an error and no data")
        elif self.status == ToolStatus.NO_RESULTS:
            if self.data not in (None, []):
                raise ValueError("NO_RESULTS cannot contain data")
            if self.error not in (None, "UNSUPPORTED_CITY_DATA"):
                raise ValueError("NO_RESULTS only accepts the public unsupported-city code")
        elif self.status == ToolStatus.SUCCESS and (self.data is None or self.data == []):
            raise ValueError("SUCCESS requires nonempty data")
        elif self.error is not None:
            raise ValueError("SUCCESS cannot carry an error")
        return self


class SearchRequest(ToolModel):
    tool_name: SearchToolName
    arguments: SearchInput


class BudgetRequest(ToolModel):
    tool_name: Literal["calculate_budget"] = "calculate_budget"
    # The tools node resolves costs after obtaining search results.
    arguments: BudgetInput | None = None


ToolRequest = SearchRequest | BudgetRequest
