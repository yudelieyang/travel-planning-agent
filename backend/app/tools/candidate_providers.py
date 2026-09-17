"""Offline candidate sources behind the existing candidate-data facade."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from app.tools.contracts import Category, TravelOption

CandidateDataMode = Literal["mock", "snapshot"]
UNIT_BY_CATEGORY = {
    "attractions": "per_person_visit",
    "hotel": "per_person_night",
    "food": "per_person_meal",
    "transport": "per_person_day",
}


class CandidateProviderError(ValueError):
    """Safe boundary error for unavailable or invalid candidate data."""


class CandidateProvider(Protocol):
    def candidates(self, destination: str, category: Category) -> list[TravelOption] | None: ...

    def source_for(self, destination: str, category: Category) -> Literal["mock", "snapshot"]: ...


class MockFixtureProvider:
    def candidates(self, destination: str, category: Category) -> list[TravelOption] | None:
        # Local import keeps the compatibility facade and provider module acyclic.
        from app.tools.candidate_data import fixture_candidates

        return fixture_candidates(destination, category)

    def source_for(self, destination: str, category: Category) -> Literal["mock"]:
        return "mock"


class SnapshotModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False, str_strip_whitespace=True)


class SnapshotCandidate(SnapshotModel):
    id: str = Field(min_length=1)
    provider_place_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    address: str | None = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    provider_category_ids: list[str] = Field(min_length=1)
    provider_category_labels: list[str] = Field(default_factory=list)
    provider_refreshed_at: datetime | None = None
    price: float = Field(ge=0)
    currency: Literal["USD"] = "USD"
    unit: Literal[
        "per_person_visit", "per_person_night", "per_person_meal", "per_person_day"
    ]
    tags: list[str]
    rating: float | None = Field(default=None, ge=0, le=5)
    review_count: int | None = Field(default=None, ge=0)
    image_url: str | None = None
    description: str | None = None
    cost_origin: Literal["planner_estimate"]
    cost_method: str = Field(min_length=1)
    cost_version: str = Field(min_length=1)

    @field_validator("provider_refreshed_at")
    @classmethod
    def provider_timestamp_is_aware(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.utcoffset() is None:
            raise ValueError("Provider timestamp must include a timezone")
        return value


class SnapshotCity(SnapshotModel):
    city: str = Field(min_length=1)
    state: str = Field(min_length=2, max_length=2)
    candidates: dict[Category, list[SnapshotCandidate]]

    @model_validator(mode="after")
    def migrated_categories_are_nonempty(self):
        if not self.candidates or any(not rows for rows in self.candidates.values()):
            raise ValueError("Every declared migrated category requires candidates")
        return self


class CandidateSnapshot(SnapshotModel):
    snapshot_version: str = Field(pattern=r"^[a-z0-9][a-z0-9._-]*$")
    snapshot_fetched_at: datetime
    provider: str = Field(min_length=1, pattern=r"^[a-z0-9][a-z0-9._-]*$")
    source: Literal["real_snapshot"]
    provider_data_timestamp: datetime | None = None
    record_count: int | None = Field(default=None, ge=1)
    category_map_version: str | None = Field(default=None, min_length=1)
    cost_method_version: str | None = Field(default=None, min_length=1)
    attribution: str | None = Field(default=None, min_length=1)
    license: str | None = Field(default=None, min_length=1)
    cities: list[SnapshotCity] = Field(min_length=1)

    @field_validator("snapshot_fetched_at", "provider_data_timestamp")
    @classmethod
    def snapshot_timestamp_is_aware(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.utcoffset() is None:
            raise ValueError("Snapshot timestamp must include a timezone")
        return value

    @model_validator(mode="after")
    def validate_identity_and_units(self):
        internal_ids = []
        provider_ids = []
        city_names = []
        for city in self.cities:
            city_names.append(city.city.casefold())
            for category, rows in city.candidates.items():
                for row in rows:
                    if row.unit != UNIT_BY_CATEGORY[category]:
                        raise ValueError("Candidate unit is incompatible with its category")
                    internal_ids.append(row.id)
                    provider_ids.append((self.provider, row.provider_place_id))
        if len(internal_ids) != len(set(internal_ids)):
            raise ValueError("Candidate ids must be unique")
        if len(provider_ids) != len(set(provider_ids)):
            raise ValueError("Provider candidate identities must be unique")
        if len(city_names) != len(set(city_names)):
            raise ValueError("Snapshot cities must be unique")
        if self.record_count is not None and self.record_count != len(internal_ids):
            raise ValueError("Snapshot record count does not match candidate rows")
        if self.provider == "openstreetmap" and any(
            re.fullmatch(r"(node|way|relation)/[1-9][0-9]*", provider_id) is None
            for _, provider_id in provider_ids
        ):
            raise ValueError("OpenStreetMap identities require element type and numeric id")
        return self


class SnapshotRoute(SnapshotModel):
    city: str = Field(min_length=1)
    category: Category
    snapshot: Path


class CandidateMigrationManifest(SnapshotModel):
    manifest_version: str = Field(pattern=r"^[a-z0-9][a-z0-9._-]*$")
    routes: list[SnapshotRoute] = Field(min_length=1)

    @model_validator(mode="after")
    def routes_are_unique(self):
        keys = [(route.city.casefold(), route.category) for route in self.routes]
        if len(keys) != len(set(keys)):
            raise ValueError("Migration manifest routes must be unique")
        return self


class RealSnapshotProvider:
    """Eagerly validated local snapshot provider; it never performs network I/O."""

    def __init__(self, path: Path):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            self.snapshot = CandidateSnapshot.model_validate(raw)
            self._validate_supported_cities()
        except (OSError, json.JSONDecodeError, ValidationError, ValueError) as exc:
            raise CandidateProviderError("Candidate snapshot unavailable or invalid") from exc

    def _validate_supported_cities(self) -> None:
        from app.tools.candidate_data import resolve_city

        for snapshot_city in self.snapshot.cities:
            registered = resolve_city(snapshot_city.city)
            if (
                registered is None
                or registered.city != snapshot_city.city
                or registered.state != snapshot_city.state
            ):
                raise ValueError("Snapshot contains an unsupported city")

    def candidates(self, destination: str, category: Category) -> list[TravelOption] | None:
        from app.tools.candidate_data import resolve_city

        registered = resolve_city(destination)
        if registered is None:
            return None
        snapshot_city = next(
            (city for city in self.snapshot.cities if city.city == registered.city), None
        )
        if snapshot_city is None:
            return []
        rows = snapshot_city.candidates.get(category, [])
        return [
            TravelOption(
                **row.model_dump(),
                destination=registered.city,
                city=registered.city,
                state=registered.state,
                category=category,
                source=self.snapshot.source,
                provider=self.snapshot.provider,
                snapshot_version=self.snapshot.snapshot_version,
                snapshot_fetched_at=self.snapshot.snapshot_fetched_at,
            )
            for row in rows
        ]

    def source_for(self, destination: str, category: Category) -> Literal["snapshot"]:
        return "snapshot"


class MixedCandidateProvider:
    """Explicitly route migrated categories to snapshot data and all others to fixtures."""

    def __init__(self, routes: dict[tuple[str, Category], RealSnapshotProvider]):
        self.routes = routes
        self.mock = MockFixtureProvider()
        if not routes or any(
            not provider.candidates(city, category)
            for (city, category), provider in routes.items()
        ):
            raise CandidateProviderError("Candidate snapshot missing a declared migrated route")

    def _provider(self, destination: str, category: Category) -> CandidateProvider:
        from app.tools.candidate_data import resolve_city

        city = resolve_city(destination)
        route = (city.city, category) if city is not None else None
        return self.routes.get(route, self.mock)

    def candidates(self, destination: str, category: Category) -> list[TravelOption] | None:
        return self._provider(destination, category).candidates(destination, category)

    def source_for(self, destination: str, category: Category) -> Literal["mock", "snapshot"]:
        return self._provider(destination, category).source_for(destination, category)


def create_candidate_provider(
    mode: CandidateDataMode, snapshot_path: Path | None = None
) -> CandidateProvider:
    if mode == "mock":
        return MockFixtureProvider()
    if snapshot_path is None:
        raise CandidateProviderError("Snapshot mode requires CANDIDATE_SNAPSHOT_PATH")
    try:
        raw = json.loads(snapshot_path.read_text(encoding="utf-8"))
        if "routes" not in raw:
            provider = RealSnapshotProvider(snapshot_path)
            routes = {
                (city.city, category): provider
                for city in provider.snapshot.cities
                for category in city.candidates
            }
        else:
            manifest = CandidateMigrationManifest.model_validate(raw)
            routes = {}
            for route in manifest.routes:
                path = route.snapshot
                if not path.is_absolute():
                    path = snapshot_path.parent / path
                routes[(route.city, route.category)] = RealSnapshotProvider(path)
        return MixedCandidateProvider(routes)
    except (OSError, json.JSONDecodeError, ValidationError, ValueError) as exc:
        raise CandidateProviderError("Candidate migration manifest unavailable or invalid") from exc
