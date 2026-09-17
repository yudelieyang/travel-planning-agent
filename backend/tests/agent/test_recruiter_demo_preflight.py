from scripts import preflight_recruiter_demo

from app.core.config import PROJECT_ROOT


def configure(monkeypatch, mode="snapshot", path=None):
    monkeypatch.setenv("POSTGRES_DB", "test")
    monkeypatch.setenv("POSTGRES_USER", "test")
    monkeypatch.setenv("POSTGRES_PASSWORD", "test")
    monkeypatch.setenv("CANDIDATE_DATA_MODE", mode)
    monkeypatch.setenv(
        "CANDIDATE_SNAPSHOT_PATH",
        str(
            path
            or PROJECT_ROOT
            / "data/travel/snapshots/openstreetmap/migration_manifest.json"
        ),
    )


def test_recruiter_demo_preflight_validates_all_manifest_routes(monkeypatch, capsys):
    configure(monkeypatch)

    assert preflight_recruiter_demo.main() == 0
    assert "36 snapshot routes" in capsys.readouterr().out


def test_recruiter_demo_preflight_rejects_mock_or_missing_snapshot(monkeypatch, capsys, tmp_path):
    configure(monkeypatch, mode="mock")
    assert preflight_recruiter_demo.main() == 1
    assert "CANDIDATE_DATA_MODE must be snapshot" in capsys.readouterr().err

    configure(monkeypatch, path=tmp_path / "missing.json")
    assert preflight_recruiter_demo.main() == 1
    assert "Candidate migration manifest unavailable or invalid" in capsys.readouterr().err
