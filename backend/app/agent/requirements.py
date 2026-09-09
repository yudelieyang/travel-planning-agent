"""Explicit requirements and a deliberately limited, offline English parser."""

import re
from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class TravelRequirements(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    destination: str | None = None
    origin: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    duration_days: int | None = Field(default=None, ge=1, le=30)
    travelers: int | None = Field(default=None, ge=1, le=20)
    budget: float | None = Field(default=None, ge=0)
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    interests: list[str] = Field(default_factory=list)
    hotel_preferences: list[str] = Field(default_factory=list)
    food_preferences: list[str] = Field(default_factory=list)
    transport_preferences: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)

    @field_validator("destination", "origin")
    @classmethod
    def normalize_place(cls, value: str | None) -> str | None:
        if not value or not value.strip():
            return None
        value = value.strip()
        return {
            "nyc": "New York City",
            "new york": "New York City",
            "new york city": "New York City",
            "boston": "Boston",
        }.get(value.lower(), value)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date:
            days = (self.end_date - self.start_date).days + 1
            if not 1 <= days <= 30:
                raise ValueError("Date range must cover 1 to 30 days, inclusive")
            if self.duration_days is not None and self.duration_days != days:
                raise ValueError("Duration conflicts with the inclusive date range")
        return self

    @property
    def trip_days(self) -> int | None:
        if self.duration_days is not None:
            return self.duration_days
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return None


class RequirementStatus(StrEnum):
    SUFFICIENT = "SUFFICIENT"
    INSUFFICIENT = "INSUFFICIENT"


class RequirementAssessment(BaseModel):
    status: RequirementStatus
    missing_fields: list[str] = Field(default_factory=list)


def assess_requirements(requirements: TravelRequirements) -> RequirementAssessment:
    missing = []
    if not requirements.destination:
        missing.append("destination")
    if requirements.trip_days is None:
        missing.append("duration")
    return RequirementAssessment(
        status=RequirementStatus.INSUFFICIENT if missing else RequirementStatus.SUFFICIENT,
        missing_fields=missing,
    )


def parse_requirements(query: str) -> TravelRequirements:
    """Recognize documented patterns; never fill missing destination/duration/party size."""
    values = {}
    place = re.search(
        r"\b(?:to|in|visit)\s+([A-Za-z][A-Za-z ]*?)"
        r"(?=\s+(?:under|for|with|from|on|starting|between)\b|[.,!?]|$)",
        query,
        re.I,
    )
    if place:
        values["destination"] = place[1].strip()
    origin = re.search(r"\bfrom\s+([A-Za-z][A-Za-z ]*?)\s+to\b", query, re.I)
    if origin:
        values["origin"] = origin[1].strip()
    duration = re.search(r"(?<![\w.])(-?\d+)\s*[- ]\s*days?\b", query, re.I)
    if duration:
        values["duration_days"] = int(duration[1])
    travelers = re.search(
        r"(?<![\w.])(-?\d+)\s+(?:travelers?|people|persons?|adults?)\b", query, re.I
    )
    if travelers:
        values["travelers"] = int(travelers[1])
    dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", query)
    if len(dates) > 2:
        raise ValueError("Provide at most a start and an end date")
    if dates:
        values["start_date"] = date.fromisoformat(dates[0])
    if len(dates) == 2:
        values["end_date"] = date.fromisoformat(dates[1])
    amount = re.search(
        r"(?:under|budget(?:\s+of)?|up to)\s*(?:(USD|EUR|GBP)\s*|([$€£])\s*)?"
        r"(-?\d[\d,]*(?:\.\d+)?)\s*(USD|EUR|GBP)?",
        query,
        re.I,
    )
    if amount:
        values["budget"] = float(amount[3].replace(",", ""))
        values["currency"] = (
            amount[1] or amount[4] or {"€": "EUR", "£": "GBP"}.get(amount[2], "USD")
        ).upper()
    vocabulary = {
        "interests": ["museums", "food", "parks", "history", "art"],
        "hotel_preferences": ["quiet", "central", "budget", "luxury"],
        "food_preferences": ["vegetarian", "vegan", "seafood"],
        "transport_preferences": ["walking", "public transit", "taxi"],
        "constraints": ["wheelchair", "no walking"],
    }
    for field, terms in vocabulary.items():
        # Monetary 'budget' is not a request for a budget hotel.
        values[field] = [
            term
            for term in terms
            if re.search(r"\b" + term + r"\b", query, re.I)
            and (term != "budget" or re.search(r"budget hotel", query, re.I))
        ]
    return TravelRequirements(**values)
