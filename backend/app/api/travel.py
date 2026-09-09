from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException

from app.agent.service import PlanRequest, PlanResponse, TravelService

router = APIRouter(prefix="/api/v1/travel", tags=["travel"])


@lru_cache
def get_travel_service() -> TravelService:
    return TravelService()


@router.post("/plan", response_model=PlanResponse)
def plan_travel(request: PlanRequest, service: TravelService = Depends(get_travel_service)):
    try:
        return service.plan(request.query)
    except ValueError as exc:
        raise HTTPException(
            status_code=422, detail="Invalid or inconsistent travel requirements"
        ) from exc
