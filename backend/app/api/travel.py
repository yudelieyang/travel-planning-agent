from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from app.agent.openai_planner import PlannerConfigurationError, create_planner
from app.agent.service import PlanRequest, PlanResponse, TravelService
from app.core.config import Settings

router = APIRouter(prefix="/api/v1/travel", tags=["travel"])


@lru_cache
def get_travel_service() -> TravelService:
    try:
        return TravelService(planner=create_planner(Settings()))
    except PlannerConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from None
    except ValidationError:
        raise HTTPException(status_code=503, detail="Invalid application configuration") from None


@router.post("/plan", response_model=PlanResponse)
def plan_travel(request: PlanRequest, service: TravelService = Depends(get_travel_service)):
    try:
        return service.plan(request.query)
    except ValueError as exc:
        raise HTTPException(
            status_code=422, detail="Invalid or inconsistent travel requirements"
        ) from exc
