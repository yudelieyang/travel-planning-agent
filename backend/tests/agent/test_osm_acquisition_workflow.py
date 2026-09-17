import argparse
import json

from scripts import acquire_osm_snapshots as acquisition


def test_batch_query_uses_explicit_boundary_and_provider_global_taxonomy():
    new_york = acquisition.build_query("New York City", "attractions")
    dc = acquisition.build_query("Washington DC", "food")

    assert "rel(175905)->.boundary" in new_york
    assert "area(3600175905)->.searchArea" in new_york
    assert 'tourism"~"^(museum|aquarium)$' in new_york
    assert 'leisure"="park' in new_york
    assert "rel(162069)->.boundary" in dc
    assert "area(3600162069)->.searchArea" in dc
    assert 'amenity"="restaurant' in dc


def test_selection_prefers_complete_metadata_and_skips_nearby_same_name_duplicate():
    raw = {
        "elements": [
            {
                "type": "node",
                "id": 1,
                "lat": 40.0,
                "lon": -73.0,
                "tags": {
                    "name": "Complete Museum",
                    "tourism": "museum",
                    "addr:housenumber": "1",
                    "addr:street": "Main Street",
                    "addr:city": "New York",
                    "addr:state": "NY",
                    "addr:postcode": "10001",
                },
            },
            {
                "type": "way",
                "id": 2,
                "center": {"lat": 40.0001, "lon": -73.0001},
                "tags": {"name": "Complete Museum", "tourism": "museum"},
            },
            {
                "type": "node",
                "id": 3,
                "lat": 40.1,
                "lon": -73.1,
                "tags": {"name": "Other Museum", "tourism": "museum"},
            },
        ]
    }

    selected, duplicates = acquisition.select_elements(raw, "attractions", 2)

    assert [row["id"] for row in selected] == [1, 3]
    assert duplicates == ["way/2 skipped near node/1 with the same normalized name"]


def test_resume_uses_raw_checkpoint_and_completed_unit_never_requests_again(tmp_path, monkeypatch):
    snapshot_root = tmp_path / "snapshots"
    source_root = tmp_path / "sources"
    cache = tmp_path / "cache"
    dataset = tmp_path / "cities.json"
    dataset.write_text(
        json.dumps(
            {
                "cities": [
                    {
                        "city": "New York City",
                        "state": "NY",
                        "candidates": {
                            "attractions": [
                                {
                                    "id": "nyc-a1",
                                    "name": "Mock",
                                    "price": 25,
                                    "currency": "USD",
                                    "unit": "per_person_visit",
                                    "tags": ["museums", "art"],
                                }
                            ]
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(acquisition, "SNAPSHOT_ROOT", snapshot_root)
    monkeypatch.setattr(acquisition, "SOURCE_ROOT", source_root)
    monkeypatch.setattr(acquisition, "DATASET_PATH", dataset)
    unit = "new_york_city_attractions_2026-09-16_v1"
    raw_path = cache / "raw" / f"{unit}.json"
    acquisition.atomic_write_json(
        raw_path,
        {
            "osm3s": {"timestamp_osm_base": "2026-09-16T00:00:00Z"},
            "elements": [
                {
                    "type": "relation",
                    "id": 175905,
                    "center": {"lat": 40.7, "lon": -74.0},
                    "tags": {
                        "name": "New York",
                        "boundary": "administrative",
                        "admin_level": "5",
                    },
                },
                {
                    "type": "node",
                    "id": 99,
                    "lat": 40.75,
                    "lon": -73.98,
                    "tags": {
                        "name": "Test Museum",
                        "tourism": "museum",
                        "addr:housenumber": "1",
                        "addr:street": "Test Street",
                        "addr:city": "New York",
                        "addr:state": "NY",
                        "addr:postcode": "10001",
                    },
                },
            ],
        },
    )
    args = argparse.Namespace(
        city="New York City",
        category="attractions",
        version="2026-09-16_v1",
        endpoint="https://invalid.example",
        cache_dir=str(cache),
        resume=True,
        force_refresh=False,
    )
    monkeypatch.setattr(
        acquisition,
        "fetch",
        lambda *_: (_ for _ in ()).throw(AssertionError("network request was made")),
    )

    snapshot, source = acquisition.run(args)
    second_snapshot, second_source = acquisition.run(args)

    assert snapshot == second_snapshot and source == second_source
    assert snapshot.exists() and source.exists()
    assert not list(snapshot.parent.glob("*.tmp*"))
    state = json.loads((cache / "state" / f"{unit}.json").read_text(encoding="utf-8"))
    assert state["status"] == "completed"


def test_resume_refetches_an_empty_raw_checkpoint(tmp_path, monkeypatch):
    snapshot_root = tmp_path / "snapshots"
    source_root = tmp_path / "sources"
    cache = tmp_path / "cache"
    dataset = tmp_path / "cities.json"
    dataset.write_text(
        json.dumps(
            {
                "cities": [
                    {
                        "city": "Miami",
                        "state": "FL",
                        "candidates": {
                            "attractions": [
                                {
                                    "id": "mia-a1",
                                    "name": "Mock",
                                    "price": 12,
                                    "currency": "USD",
                                    "unit": "per_person_visit",
                                    "tags": ["museums"],
                                }
                            ]
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(acquisition, "SNAPSHOT_ROOT", snapshot_root)
    monkeypatch.setattr(acquisition, "SOURCE_ROOT", source_root)
    monkeypatch.setattr(acquisition, "DATASET_PATH", dataset)
    unit = "miami_attractions_2026-09-16_v1"
    acquisition.atomic_write_json(cache / "raw" / f"{unit}.json", {"elements": []})
    response = {
        "osm3s": {"timestamp_osm_base": "2026-09-16T00:00:00Z"},
        "elements": [
            {
                "type": "relation",
                "id": 1216769,
                "center": {"lat": 25.77, "lon": -80.2},
                "tags": {
                    "name": "Miami",
                    "boundary": "administrative",
                    "admin_level": "8",
                },
            },
            {
                "type": "node",
                "id": 42,
                "lat": 25.78,
                "lon": -80.19,
                "tags": {
                    "name": "Test Museum",
                    "tourism": "museum",
                    "addr:housenumber": "1",
                    "addr:street": "Test Street",
                    "addr:city": "Miami",
                    "addr:state": "FL",
                },
            },
        ],
    }
    calls = []

    def fetch(*_):
        calls.append(True)
        return json.dumps(response).encode()

    monkeypatch.setattr(acquisition, "fetch", fetch)
    args = argparse.Namespace(
        city="Miami",
        category="attractions",
        version="2026-09-16_v1",
        endpoint="https://example.invalid",
        cache_dir=str(cache),
        resume=True,
        force_refresh=False,
    )

    snapshot, source = acquisition.run(args)

    assert calls == [True]
    assert snapshot.exists() and source.exists()
