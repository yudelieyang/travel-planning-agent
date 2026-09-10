"""Replaceable requirements extraction; no LLM implementation in this phase."""

from typing import Protocol

from app.agent.requirements import TravelRequirements, parse_requirements


class RequirementsExtractorProtocol(Protocol):
    def extract(self, query: str) -> TravelRequirements: ...


class RuleBasedRequirementsExtractor:
    def extract(self, query: str) -> TravelRequirements:
        return parse_requirements(query)
