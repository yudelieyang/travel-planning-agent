"""Process health only; no external services are contacted."""

from fastapi import FastAPI

app = FastAPI(title="Travel Agent Backend")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "travel-agent-backend"}
