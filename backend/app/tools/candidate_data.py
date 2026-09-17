"""Validated, cached access to the controlled US demo candidate dataset."""

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.tools.contracts import Category, TravelOption

if TYPE_CHECKING:
    from app.tools.candidate_providers import CandidateProvider

CANDIDATE_DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "travel" / "us" / "cities.json"


class FixtureModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class CandidateFixture(FixtureModel):
    id: str
    name: str
    price: float = Field(ge=0)
    currency: Literal["USD"] = "USD"
    unit: Literal["per_person_visit", "per_person_night", "per_person_meal", "per_person_day"]
    tags: list[str]
    rating: float | None = Field(default=None, ge=0, le=5)
    review_count: int | None = Field(default=None, ge=0)
    image_url: str | None = None
    description: str | None = None


class CityFixture(FixtureModel):
    city: str
    state: str = Field(min_length=2, max_length=2)
    aliases: list[str]
    candidates: dict[Category, list[CandidateFixture]]

    @model_validator(mode="after")
    def has_every_category(self):
        expected = {"attractions", "hotel", "food", "transport"}
        if set(self.candidates) != expected or any(not rows for rows in self.candidates.values()):
            raise ValueError("Every city requires nonempty candidates for all four categories")
        return self


class CandidateDataset(FixtureModel):
    dataset: str
    source: Literal["controlled_mock_fixture"]
    cities: list[CityFixture]

    @model_validator(mode="after")
    def unique_identifiers(self):
        ids = [row.id for city in self.cities for rows in city.candidates.values() for row in rows]
        if len(ids) != len(set(ids)):
            raise ValueError("Candidate ids must be unique")
        owners = {}
        for city in self.cities:
            for alias in [city.city, *city.aliases]:
                key = location_key(alias)
                if key in owners and owners[key] != city.city:
                    raise ValueError("A city alias cannot resolve to multiple cities")
                owners[key] = city.city
        return self


def location_key(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def preference_key(value: str) -> str:
    value = location_key(value)
    return {"zoos": "zoo"}.get(value, value)


@lru_cache(maxsize=1)
def load_candidate_dataset() -> CandidateDataset:
    raw = json.loads(CANDIDATE_DATA_PATH.read_text(encoding="utf-8"))
    return CandidateDataset.model_validate(raw)


def resolve_city(destination: str) -> CityFixture | None:
    key = location_key(destination)
    for city in load_candidate_dataset().cities:
        if key in {location_key(alias) for alias in [city.city, *city.aliases]}:
            return city
    return None


def city_at_start(value: str) -> tuple[CityFixture, int] | None:
    """Resolve a fixture alias and its source span at the start of shorthand input."""
    matches = []
    for city in load_candidate_dataset().cities:
        for alias in [city.city, *city.aliases]:
            alias_key = location_key(alias)
            pattern = r"^" + r"[\s,.]+".join(map(re.escape, alias_key.split())) + r"\b"
            match = re.match(pattern, value, re.IGNORECASE)
            if match:
                matches.append((match.end(), city))
    if not matches:
        return None
    length, city = max(matches, key=lambda item: item[0])
    return city, length


def fixture_candidates(destination: str, category: Category) -> list[TravelOption] | None:
    """Normalize controlled fixture rows without applying search or ranking policy."""
    city = resolve_city(destination)
    if city is None:
        return None
    return [
        TravelOption(
            **row.model_dump(),
            destination=city.city,
            city=city.city,
            state=city.state,
            category=category,
            source=load_candidate_dataset().source,
        )
        for row in city.candidates[category]
    ]


def candidates_for(
    destination: str,
    category: Category,
    *,
    max_price: float | None = None,
    preferences: list[str] | None = None,
    provider: "CandidateProvider | None" = None,
) -> list[TravelOption] | None:
    """Compatibility facade: provider lookup, hard eligibility, then stable soft ranking."""
    if provider is None:
        from app.tools.candidate_providers import MockFixtureProvider

        provider = MockFixtureProvider()
    rows = provider.candidates(destination, category)
    if rows is None:
        return None
    wanted = [preference_key(value) for value in preferences or []]
    options = []
    for row in rows:
        if max_price is not None and row.price > max_price:
            continue
        tags = {preference_key(tag) for tag in row.tags}
        matches = [value for value in wanted if value in tags]
        options.append(row.model_copy(update={"preference_matches": matches}))
    return sorted(options, key=lambda row: (-len(row.preference_matches), row.price, row.id))
