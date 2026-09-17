"""Explicit, resumable OpenStreetMap snapshot acquisition for Phase O5.

This development tool is never imported by application runtime code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from math import asin, cos, radians, sin, sqrt
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = REPO_ROOT / "data/travel/us/cities.json"
SNAPSHOT_ROOT = REPO_ROOT / "data/travel/snapshots/openstreetmap"
SOURCE_ROOT = REPO_ROOT / "data/travel/sources/openstreetmap"
DEFAULT_ENDPOINT = "https://overpass-api.de/api/interpreter"
DEFAULT_VERSION = "2026-09-16_v1"
USER_AGENT = "TravelPlanningAgent-O5-Snapshot/1.0 (one-time educational data acquisition)"
COST_METHOD = "legacy_demo_cost_preserved_for_phase_o_migration"

CATEGORY_NAMES = {
    "attractions": ("attractions", "attractions", "osm_attractions_v1"),
    "hotel": ("hotels", "hotels", "osm_hotel_v1"),
    "food": ("food", "food", "osm_food_v1"),
}

# Explicit administrative relations are validated again from every raw response.
BOUNDARIES = {
    "New York City": {"relation_id": 175905, "name": "New York", "admin_level": "5"},
    "Chicago": {"relation_id": 122604, "name": "Chicago", "admin_level": "8"},
    "Washington DC": {
        "relation_id": 162069,
        "name": "District of Columbia",
        "admin_level": "4",
    },
    "Miami": {"relation_id": 1216769, "name": "Miami", "admin_level": "8"},
    "Denver": {
        "relation_id": 1411339,
        "name": "Denver",
        "admin_level": "6",
        "query_locality": "Denver",
        "bbox": (39.6143008, -105.1098845, 39.9142087, -104.5996997),
    },
    "Seattle": {
        "relation_id": 237385,
        "name": "Seattle",
        "admin_level": "8",
        "query_locality": "Seattle",
    },
    "San Francisco": {
        "relation_id": 111968,
        "name": "San Francisco",
        "admin_level": "6",
        "query_locality": "San Francisco",
    },
    "Los Angeles": {
        "relation_id": 207359,
        "name": "Los Angeles",
        "admin_level": "8",
        "query_locality": "Los Angeles",
        "bbox": (33.659541, -118.6681798, 34.337306, -118.1552983),
        "bbox_attractions": True,
    },
    "Las Vegas": {
        "relation_id": 170117,
        "name": "Las Vegas",
        "admin_level": "8",
        "query_locality": "Las Vegas",
        "bbox": (36.129554, -115.406575, 36.401481, -115.062066),
    },
}


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", normalized.casefold()).strip("_")


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    )
    temporary = Path(handle.name)
    try:
        with handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def atomic_write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        "wb", dir=path.parent, prefix=f".{path.name}.", delete=False
    )
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_dataset() -> dict[str, Any]:
    return json.loads(DATASET_PATH.read_text(encoding="utf-8"))


def fixture(city: str, category: str) -> tuple[str, list[dict[str, Any]]]:
    for item in load_dataset()["cities"]:
        if item["city"] == city:
            return item["state"], item["candidates"][category]
    raise ValueError(f"Unsupported city: {city}")


def build_query(city: str, category: str) -> str:
    relation_id = BOUNDARIES[city]["relation_id"]
    use_bbox = "bbox" in BOUNDARIES[city] and (
        category != "attractions" or BOUNDARIES[city].get("bbox_attractions", False)
    )
    if use_bbox:
        boundary = f"rel({relation_id})->.boundary;"
        scope = ",".join(str(value) for value in BOUNDARIES[city]["bbox"])
    else:
        boundary = (
            f"rel({relation_id})->.boundary;"
            f"area({3_600_000_000 + relation_id})->.searchArea;"
        )
        scope = "area.searchArea"
    if category == "attractions":
        locality = BOUNDARIES[city].get("query_locality") if use_bbox else None
        locality_filter = (
            f'["addr:city"="{locality}"]["addr:housenumber"]["addr:street"]'
            if locality
            else ""
        )
        category_query = (
            f'nwr({scope})["name"]["tourism"~"^(museum|aquarium)$"]{locality_filter};'
            f'nwr({scope})["name"]["leisure"="park"]{locality_filter};'
        )
    elif category == "hotel":
        locality = BOUNDARIES[city].get("query_locality")
        locality_filter = f'["addr:city"="{locality}"]' if locality else (
            '["addr:housenumber"]["addr:street"]'
        )
        category_query = (
            f'node({scope})["name"]["tourism"="hotel"]{locality_filter};'
            f'way({scope})["name"]["tourism"="hotel"]{locality_filter};'
        )
    else:
        locality = BOUNDARIES[city].get("query_locality")
        locality_filter = f'["addr:city"="{locality}"]' if locality else ""
        category_query = (
            f'node({scope})["name"]["amenity"="restaurant"]'
            f'{locality_filter}["addr:housenumber"]["addr:street"];'
            f'way({scope})["name"]["amenity"="restaurant"]'
            f'{locality_filter}["addr:housenumber"]["addr:street"];'
        )
    return (
        "[out:json][timeout:180];"
        + boundary
        + "(rel.boundary;"
        + category_query
        + ");out center tags qt;"
    )


def fetch(endpoint: str, query: str) -> bytes:
    body = urllib.parse.urlencode({"data": query}).encode()
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=240) as response:  # noqa: S310
        return response.read()


def coordinates(element: dict[str, Any]) -> tuple[float, float] | None:
    source = element.get("center", element)
    lat, lon = source.get("lat"), source.get("lon")
    if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return float(lat), float(lon)
    return None


def observed(tags: dict[str, str], key: str) -> str | None:
    return tags.get(key) or tags.get(f"contact:{key.removeprefix('addr:')}")


def address(tags: dict[str, str]) -> str | None:
    if tags.get("addr:full"):
        return tags["addr:full"].strip()
    number = observed(tags, "addr:housenumber")
    street = observed(tags, "addr:street")
    locality = [
        observed(tags, "addr:city"),
        observed(tags, "addr:state"),
        observed(tags, "addr:postcode"),
    ]
    first = " ".join(part for part in (number, street) if part)
    tail = " ".join(part for part in locality if part)
    value = ", ".join(part for part in (first, tail) if part)
    return value or None


def is_boundary(element: dict[str, Any]) -> bool:
    return element.get("tags", {}).get("boundary") == "administrative"


def category_match(element: dict[str, Any], category: str) -> bool:
    tags = element.get("tags", {})
    if not tags.get("name") or coordinates(element) is None:
        return False
    if category == "attractions":
        return tags.get("tourism") in {"museum", "aquarium"} or tags.get("leisure") == "park"
    if category == "hotel":
        return tags.get("tourism") == "hotel"
    return tags.get("amenity") == "restaurant"


def is_closed(tags: dict[str, str]) -> bool:
    keys = " ".join(tags).casefold()
    return any(word in keys for word in ("disused:", "abandoned:", "demolished:", "razed:"))


def quality(element: dict[str, Any], category: str) -> tuple[int, str, str, int]:
    tags = element["tags"]
    score = 0
    if observed(tags, "addr:housenumber"):
        score += 4
    if observed(tags, "addr:street"):
        score += 4
    if observed(tags, "addr:city"):
        score += 2
    if observed(tags, "addr:state"):
        score += 1
    if observed(tags, "addr:postcode"):
        score += 1
    if tags.get("website") or tags.get("contact:website"):
        score += 2
    if tags.get("wikidata"):
        score += 1
    if category == "food" and (tags.get("cuisine") or any(k.startswith("diet:") for k in tags)):
        score += 3
    if category == "hotel" and tags.get("brand"):
        score += 1
    if category == "attractions" and tags.get("tourism") in {"museum", "aquarium"}:
        score += 2
    return (-score, normalize_name(tags["name"]), element["type"], int(element["id"]))


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def distance_meters(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1, lat2, lon2 = map(radians, (*a, *b))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    value = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 12_742_000 * asin(sqrt(value))


def select_elements(
    raw: dict[str, Any], category: str, count: int
) -> tuple[list[dict[str, Any]], list[str]]:
    candidates = [
        element
        for element in raw.get("elements", [])
        if category_match(element, category) and not is_closed(element.get("tags", {}))
    ]
    selected: list[dict[str, Any]] = []
    duplicate_notes: list[str] = []
    for element in sorted(candidates, key=lambda item: quality(item, category)):
        name = normalize_name(element["tags"]["name"])
        point = coordinates(element)
        duplicate = next(
            (
                prior
                for prior in selected
                if normalize_name(prior["tags"]["name"]) == name
                and distance_meters(coordinates(prior), point) < 100
            ),
            None,
        )
        if duplicate:
            duplicate_notes.append(
                f"{element['type']}/{element['id']} skipped near "
                f"{duplicate['type']}/{duplicate['id']} with the same normalized name"
            )
            continue
        selected.append(element)
        if len(selected) == count:
            break
    if len(selected) != count:
        raise ValueError(f"Needed {count} valid {category} candidates; found {len(selected)}")
    return selected, duplicate_notes


def provider_metadata(element: dict[str, Any], category: str) -> tuple[list[str], list[str]]:
    tags = element["tags"]
    if category == "attractions":
        if tags.get("tourism") == "museum":
            return ["tourism=museum"], ["Museum"]
        if tags.get("tourism") == "aquarium":
            return ["tourism=aquarium"], ["Aquarium"]
        return ["leisure=park"], ["Park"]
    if category == "hotel":
        return ["tourism=hotel"], ["Hotel"]
    ids, labels = ["amenity=restaurant"], ["Restaurant"]
    for cuisine in tags.get("cuisine", "").split(";"):
        cuisine = cuisine.strip().casefold()
        if cuisine and f"cuisine={cuisine}" not in ids:
            ids.append(f"cuisine={cuisine}")
            labels.append(f"Cuisine: {cuisine.replace('_', ' ').title()}")
    for key, label in (("diet:vegetarian", "Vegetarian"), ("diet:vegan", "Vegan")):
        value = tags.get(key)
        if value:
            ids.append(f"{key}={value.casefold()}")
            labels.append(f"{label} {'only' if value == 'only' else 'options'}")
    return ids, labels


def snapshot_candidate(
    controlled: dict[str, Any], element: dict[str, Any], category: str
) -> dict[str, Any]:
    lat, lon = coordinates(element)
    ids, labels = provider_metadata(element, category)
    return {
        "id": controlled["id"],
        "provider_place_id": f"{element['type']}/{element['id']}",
        "name": element["tags"]["name"],
        "address": address(element["tags"]),
        "latitude": lat,
        "longitude": lon,
        "provider_category_ids": ids,
        "provider_category_labels": labels,
        "price": controlled["price"],
        "currency": controlled.get("currency", "USD"),
        "unit": controlled["unit"],
        "tags": controlled["tags"],
        "cost_origin": "planner_estimate",
        "cost_method": COST_METHOD,
        "cost_version": "phase_o_v1",
    }


def artifact_paths(city: str, category: str, version: str) -> tuple[Path, Path]:
    city_slug = slug(city)
    directory_name, file_name, _ = CATEGORY_NAMES[category]
    snapshot_version = f"osm_{city_slug}_{directory_name}_{version}"
    return (
        SNAPSHOT_ROOT / snapshot_version / f"{city_slug}_{file_name}.json",
        SOURCE_ROOT / snapshot_version / f"{city_slug}_{file_name}_selected.json",
    )


def validate_snapshot(path: Path) -> None:
    backend = str(REPO_ROOT / "backend")
    if backend not in sys.path:
        sys.path.insert(0, backend)
    from app.tools.candidate_providers import RealSnapshotProvider

    RealSnapshotProvider(path)


def run(args: argparse.Namespace) -> tuple[Path, Path]:
    state_code, controlled = fixture(args.city, args.category)
    snapshot_path, source_path = artifact_paths(args.city, args.category, args.version)
    cache_root = Path(args.cache_dir).resolve()
    unit = f"{slug(args.city)}_{args.category}_{args.version}"
    raw_path = cache_root / "raw" / f"{unit}.json"
    state_path = cache_root / "state" / f"{unit}.json"

    existing_state = (
        json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else None
    )
    complete = (
        (snapshot_path.exists() and source_path.exists())
        or existing_state
        and existing_state.get("status") == "completed"
    )
    if not args.force_refresh and complete:
        if args.resume and snapshot_path.exists() and source_path.exists():
            print(f"Already complete; no request made: {unit}")
            return snapshot_path, source_path
        raise FileExistsError(f"Completed acquisition exists; use --force-refresh: {unit}")
    if (
        not args.force_refresh
        and not args.resume
        and (snapshot_path.exists() or source_path.exists() or raw_path.exists())
    ):
        raise FileExistsError(f"Partial acquisition exists; use --resume: {unit}")

    query = build_query(args.city, args.category)
    acquired_at = utc_now()
    state = {
        "unit": unit,
        "city": args.city,
        "category": args.category,
        "version": args.version,
        "status": "started",
        "updated_at": acquired_at,
        "raw_path": str(raw_path),
        "query": query,
    }
    atomic_write_json(state_path, state)
    try:
        reuse_raw = args.resume and raw_path.exists() and not args.force_refresh
        if reuse_raw:
            payload = raw_path.read_bytes()
            raw = json.loads(payload)
            reuse_raw = bool(raw.get("elements"))
        if not reuse_raw:
            payload = fetch(args.endpoint, query)
            raw = json.loads(payload)
            if not raw.get("elements"):
                raise ValueError("Overpass response has no elements")
            atomic_write_bytes(raw_path, payload)
        raw = json.loads(payload)
        boundaries = [item for item in raw["elements"] if is_boundary(item)]
        if len(boundaries) != 1:
            raise ValueError(f"Expected one administrative boundary, got {len(boundaries)}")
        expected_boundary = BOUNDARIES[args.city]
        actual_boundary = boundaries[0]
        if (
            actual_boundary["type"] != "relation"
            or actual_boundary["id"] != expected_boundary["relation_id"]
            or actual_boundary.get("tags", {}).get("name") != expected_boundary["name"]
            or actual_boundary.get("tags", {}).get("admin_level")
            != expected_boundary["admin_level"]
        ):
            raise ValueError("Administrative boundary identity does not match city configuration")
        state.update(
            status="acquired",
            updated_at=utc_now(),
            raw_sha256=sha256_bytes(payload),
            raw_bytes=len(payload),
        )
        atomic_write_json(state_path, state)

        selected, duplicate_notes = select_elements(raw, args.category, len(controlled))
        snapshot_version = snapshot_path.parent.name
        _, _, map_version = CATEGORY_NAMES[args.category]
        snapshot = {
            "snapshot_version": snapshot_version,
            "snapshot_fetched_at": acquired_at,
            "provider": "openstreetmap",
            "source": "real_snapshot",
            "provider_data_timestamp": raw.get("osm3s", {}).get("timestamp_osm_base"),
            "record_count": len(controlled),
            "category_map_version": map_version,
            "cost_method_version": "phase_o_v1",
            "attribution": "© OpenStreetMap contributors",
            "license": "ODbL",
            "cities": [
                {
                    "city": args.city,
                    "state": state_code,
                    "candidates": {
                        args.category: [
                            snapshot_candidate(row, element, args.category)
                            for row, element in zip(controlled, selected, strict=True)
                        ]
                    },
                }
            ],
        }
        source = {
            "endpoint": args.endpoint,
            "acquired_at": acquired_at,
            "osm_base_timestamp": raw.get("osm3s", {}).get("timestamp_osm_base"),
            "administrative_boundary": {
                "provider_place_id": f"{boundaries[0]['type']}/{boundaries[0]['id']}",
                "name": boundaries[0].get("tags", {}).get("name"),
                "admin_level": boundaries[0].get("tags", {}).get("admin_level"),
            },
            "query": query,
            "raw_temporary_path": str(raw_path),
            "raw_response_sha256": sha256_bytes(payload),
            "raw_response_bytes": len(payload),
            "returned_element_count": len(raw["elements"]),
            "selected_count": len(selected),
            "duplicate_resolution": duplicate_notes,
            "copyright": (
                "The data included in this document is from www.openstreetmap.org. "
                "The data is made available under ODbL."
            ),
            "elements": selected,
        }

        temporary_snapshot = snapshot_path.with_suffix(".validated.tmp.json")
        atomic_write_json(temporary_snapshot, snapshot)
        try:
            validate_snapshot(temporary_snapshot)
            atomic_write_json(source_path, source)
            os.replace(temporary_snapshot, snapshot_path)
        finally:
            temporary_snapshot.unlink(missing_ok=True)
        state.update(
            status="completed",
            updated_at=utc_now(),
            snapshot_path=str(snapshot_path),
            source_path=str(source_path),
            snapshot_sha256=hashlib.sha256(snapshot_path.read_bytes()).hexdigest(),
        )
        atomic_write_json(state_path, state)
        return snapshot_path, source_path
    except Exception as exc:
        state.update(status="failed", updated_at=utc_now(), error=f"{type(exc).__name__}: {exc}")
        atomic_write_json(state_path, state)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--city", required=True, choices=sorted(BOUNDARIES))
    parser.add_argument("--category", required=True, choices=sorted(CATEGORY_NAMES))
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument(
        "--cache-dir",
        default=str(Path(tempfile.gettempdir()) / "travel-planning-agent-osm-o5"),
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--force-refresh", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    snapshot_file, source_file = run(parse_args())
    print(snapshot_file)
    print(source_file)
