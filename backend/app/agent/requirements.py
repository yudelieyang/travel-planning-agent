"""Explicit requirements and a deliberately limited, offline English parser."""

import re
from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.budget import BudgetScope


class TravelRequirements(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    destination: str | None = None
    origin: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    duration_days: int | None = Field(default=None, ge=1, le=30)
    travelers: int | None = Field(default=None, ge=1, le=20)
    budget_amount: float | None = Field(default=None, ge=0)
    budget_scope: BudgetScope = BudgetScope.UNKNOWN
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
    query = " ".join(query.replace("’", "'").split())
    values = {}
    place = re.search(
        r"\b(?:to|in|visit)\s+([A-Za-z][A-Za-z ]*?)"
        r"(?=\s+(?:under|for|with|from|on|starting|between|around|but|budget)\b|[.,!?;]|$)",
        query,
        re.I,
    )
    if place:
        values["destination"] = place[1].strip()
    else:
        # Shorthand supports existing city aliases only; no arbitrary adjective becomes a city.
        short = re.match(r"(new york city|new york|nyc|boston)\b", query, re.I)
        if short:
            values["destination"] = short[1]
            if re.match(r"\s+or\b", query[short.end() :], re.I):
                values["destination"] = None
                values["constraints"] = ["ambiguous destination"]
    destination = values.get("destination")
    if destination and re.search(r"\bor\b", destination, re.I):
        values["destination"] = None
        values["constraints"] = ["ambiguous destination"]
    elif destination and re.match(
        r"(?:somewhere|anywhere|rent|eat|stay|book)\b", destination, re.I
    ):
        values["destination"] = None
    origin = re.search(r"\bfrom\s+([A-Za-z][A-Za-z ]*?)\s+to\b", query, re.I)
    if origin:
        values["origin"] = origin[1].strip()
    duration = re.search(rf"(?<![\w.])({NUMBER})\s*[- ]\s*days?\b", query, re.I)
    if duration:
        values["duration_days"] = number_value(duration[1])
    travelers = re.search(
        rf"(?<![\w.])({NUMBER})\s+(?:travelers?|people|persons?|adults?)\b", query, re.I
    )
    if not travelers:
        travelers = re.search(rf"\bfamily of\s+({NUMBER})\b", query, re.I)
    if not travelers:
        travelers = re.search(
            rf"\bfor\s+({NUMBER})(?=\s*(?:[.,;!?]|$|under\b|with\b))", query, re.I
        )
    if travelers:
        values["travelers"] = number_value(travelers[1])
    elif re.search(r"\b(?:traveling|travelling) alone\b", query, re.I):
        values["travelers"] = 1
    elif re.search(r"\bme and my partner\b", query, re.I):
        values["travelers"] = 2
    dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", query)
    if len(dates) > 2:
        raise ValueError("Provide at most a start and an end date")
    if dates:
        values["start_date"] = date.fromisoformat(dates[0])
    if len(dates) == 2:
        values["end_date"] = date.fromisoformat(dates[1])
    for amount in re.finditer(
        r"(?:(?P<intro>under|(?:total\s+)?budget(?:\s+(?:of|is))?|up to|around)\s*)?"
        r"(?:(?P<code>USD|EUR|GBP)\s*|(?P<symbol>[$€£])\s*)?"
        r"(?P<amount>-?\d[\d,]*(?:\.\d+)?)\s*(?P<currency>USD|EUR|GBP)?",
        query,
        re.I,
    ):
        if not any(amount[k] for k in ("intro", "code", "symbol", "currency")):
            continue  # A duration, date, or party count alone is not a monetary amount.
        values["budget_amount"] = float(amount["amount"].replace(",", ""))
        scope_text = query[amount.end() :].lstrip()
        if re.match(r"(?:per (?:person|traveler)|each)\b", scope_text, re.I):
            values["budget_scope"] = BudgetScope.PER_PERSON
        elif re.match(r"(?:total|for (?:the )?(?:whole|entire) trip)\b", scope_text, re.I) or (
            amount["intro"] and "total" in amount["intro"].lower()
        ):
            values["budget_scope"] = BudgetScope.TOTAL_TRIP
        if amount["intro"] and amount["intro"].lower() == "around":
            values.setdefault("constraints", []).append("approximate budget")
        values["currency"] = (
            amount["code"]
            or amount["currency"]
            or {"€": "EUR", "£": "GBP"}.get(amount["symbol"], "USD")
        ).upper()
        break
    vocabulary = {
        "interests": ["museums", "food", "parks", "history", "art"],
        "hotel_preferences": ["quiet", "central", "budget", "luxury"],
        "food_preferences": ["vegetarian", "vegan", "seafood"],
        "transport_preferences": ["walking", "public transit", "taxi"],
    }
    clauses = re.split(r"[.!?;]|\b(?:but|however)\b", query.lower())
    constraints = values.setdefault("constraints", [])
    for field, terms in vocabulary.items():
        values[field] = []
        for term in terms:
            for clause in clauses:
                match = re.search(r"\b" + re.escape(term) + r"\b", clause)
                if not match or (term == "budget" and not re.search(r"budget hotels?", clause)):
                    continue
                if re.search(NEGATOR, clause[: match.start()]):
                    constraints.append("no walking" if term == "walking" else "avoid " + term)
                elif term not in values[field]:
                    values[field].append(term)
    for clause in clauses:
        for term, label in NEGATIVE_TERMS.items():
            match = re.search(term, clause)
            if match and re.search(NEGATOR, clause[: match.start()]):
                constraints.append(label)
        if re.search(r"\bwheelchair\b", clause):
            constraints.append("wheelchair")
        must = re.search(r"\bmust\s+.+", clause)
        if must:
            constraints.append(must[0].strip())
        if re.search(r"\b(?:cheap|affordable)\b", clause):
            constraints.append(clause.strip())
    values["constraints"] = list(dict.fromkeys(constraints))
    return TravelRequirements(**values)


NUMBER_WORDS = dict(
    zip(
        "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split(),
        range(1, 21),
        strict=True,
    )
)
NUMBER = r"-?\d+|" + "|".join(NUMBER_WORDS)
NEGATOR = r"\b(?:don't|do not|no|not|avoid|without|never)\b"
NEGATIVE_TERMS = {
    r"\bnightlife\b": "no nightlife",
    r"\bmeat\b": "no meat",
    r"\b(?:rent a car|rental car)\b": "no rental car",
    r"\bexpensive restaurants?\b": "avoid expensive restaurants",
}


def number_value(token: str) -> int:
    return NUMBER_WORDS[token.lower()] if token.lower() in NUMBER_WORDS else int(token)
