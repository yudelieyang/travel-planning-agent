"""Offline framework checks and localhost infrastructure smoke tests; no LLM calls."""

import importlib
import sys
from pathlib import Path
from uuid import uuid4

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# Local to this process; no system PYTHONPATH changes.
sys.path.insert(0, str(PROJECT_ROOT / "backend"))


def check_python() -> None:
    if sys.version_info[:2] != (3, 11):
        raise RuntimeError("Python 3.11 is required")


def check_virtual_environment() -> None:
    if sys.prefix == sys.base_prefix or Path(sys.prefix).resolve() != PROJECT_ROOT / ".venv":
        raise RuntimeError("Activate the project .venv")


def check_configuration():
    from app.core.config import Settings

    if not (PROJECT_ROOT / ".env").is_file():
        raise RuntimeError("Copy .env.example to .env")
    # Infrastructure verification deliberately ignores any process OpenAI key.
    settings = Settings(openai_api_key="")
    if not settings.postgres_password.get_secret_value():
        raise RuntimeError("PostgreSQL password is required")
    return settings


def check_postgres(settings) -> None:
    import psycopg

    with psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password.get_secret_value(),
        connect_timeout=5,
        options="-c statement_timeout=5000",
    ) as connection:
        if connection.execute("SELECT 1").fetchone() != (1,):
            raise RuntimeError("Unexpected SELECT result")


def check_redis(settings) -> None:
    from redis import Redis

    key = f"environment_test:{uuid4().hex}"
    with Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        socket_connect_timeout=5,
        socket_timeout=5,
        decode_responses=True,
    ) as client:
        if not client.ping():
            raise RuntimeError("PING failed")
        try:
            client.set(key, "ok", ex=60)
            if client.get(key) != "ok":
                raise RuntimeError("Redis round trip failed")
        finally:
            client.delete(key)
        if client.exists(key):
            raise RuntimeError("Redis cleanup failed")


def check_chroma(settings) -> None:
    import chromadb
    from chromadb.config import Settings as ChromaSettings

    client = chromadb.PersistentClient(
        path=str(settings.chroma_persist_directory),
        settings=ChromaSettings(anonymized_telemetry=False),
    )
    name = f"environment-test-{uuid4().hex}"
    collection = client.create_collection(name=name, embedding_function=None)
    try:
        collection.add(ids=["smoke"], documents=["test document"], embeddings=[[1.0, 0.0, 0.0]])
        if collection.get(ids=["smoke"])["documents"] != ["test document"]:
            raise RuntimeError("Chroma read failed")
        collection.update(ids=["smoke"], documents=["updated"], embeddings=[[1.0, 0.0, 0.0]])
        result = collection.query(query_embeddings=[[1.0, 0.0, 0.0]], n_results=1)
        if result["ids"] != [["smoke"]] or result["documents"] != [["updated"]]:
            raise RuntimeError("Chroma query failed")
        collection.delete(ids=["smoke"])
        if collection.count() != 0:
            raise RuntimeError("Chroma document deletion failed")
    finally:
        client.delete_collection(name)
    if any(item.name == name for item in client.list_collections()):
        raise RuntimeError("Chroma collection cleanup failed")


def main() -> int:
    checks = [
        ("Python 3.11", check_python),
        ("Virtual environment", check_virtual_environment),
        ("Configuration", check_configuration),
        ("LangChain", lambda: importlib.import_module("langchain")),
        ("LangGraph", lambda: importlib.import_module("langgraph")),
        ("LangChain OpenAI", lambda: importlib.import_module("langchain_openai")),
    ]
    settings = None
    for label, check in checks:
        try:
            result = check()
            if label == "Configuration":
                settings = result
        except Exception as exc:
            # Exception text may contain connection details or secrets; never print it.
            print(f"[FAIL] {label} ({type(exc).__name__}); check setup in README")
            return 1
        print(f"[PASS] {label}")
    for label, check in [
        ("PostgreSQL", check_postgres),
        ("Redis", check_redis),
        ("ChromaDB", check_chroma),
    ]:
        try:
            check(settings)
        except Exception as exc:
            print(f"[FAIL] {label} ({type(exc).__name__}); check setup in README")
            return 1
        print(f"[PASS] {label}")
    print("ENVIRONMENT CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
