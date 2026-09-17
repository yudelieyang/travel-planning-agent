from functools import lru_cache, partial

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from app.agent.openai_planner import PlannerConfigurationError, create_planner
from app.agent.semantic_extractor import create_semantic_extractor
from app.agent.service import PlanRequest, PlanResponse, TravelService
from app.core.config import Settings
from app.tools.candidate_providers import CandidateProviderError, create_candidate_provider
from app.tools.mock import run_tool

router = APIRouter(prefix="/api/v1/travel", tags=["travel"])


@lru_cache
def get_travel_service() -> TravelService:
    try:
        settings = Settings()
        provider = create_candidate_provider(
            settings.candidate_data_mode, settings.candidate_snapshot_path
        )
        return TravelService(
            planner=create_planner(settings),
            tool_runner=partial(run_tool, provider=provider),
            semantic_extractor=create_semantic_extractor(settings),
            semantic_augmentation_enabled=settings.semantic_augmentation_mode == "hybrid",
        )
    except PlannerConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from None
    except CandidateProviderError as exc:
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
