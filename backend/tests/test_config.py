from app.core.config import PROJECT_ROOT, Settings


def test_config_resolves_paths_from_project_root(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    settings = Settings(openai_api_key="")
    assert settings.model_config["env_file"] == PROJECT_ROOT / ".env"
    assert settings.chroma_persist_directory == PROJECT_ROOT / "chroma_data"
    assert settings.openai_api_key.get_secret_value() == ""


def test_secrets_are_redacted():
    settings = Settings(
        _env_file=None,
        postgres_db="test",
        postgres_user="test",
        postgres_password="test-only-password",
        openai_api_key="",
    )
    assert "test-only-password" not in repr(settings)
