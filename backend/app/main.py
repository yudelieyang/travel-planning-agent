"""Local health and offline single-planner vertical slice."""

from fastapi import FastAPI

from app.api.travel import router as travel_router

app = FastAPI(title="Travel Agent Backend")
app.include_router(travel_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "travel-agent-backend"}
