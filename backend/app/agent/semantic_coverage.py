"""Deterministic gate for optional semantic augmentation; it never changes requirements."""

import re
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from app.agent.requirements import TravelRequirements


class CoverageReason(StrEnum):
    AMBIGUOUS_SCOPE = "AMBIGUOUS_SCOPE"
    UNSUPPORTED_HARD_REQUIREMENT = "UNSUPPORTED_HARD_REQUIREMENT"
    TRADEOFF_LANGUAGE = "TRADEOFF_LANGUAGE"
    MONETARY_SEMANTIC_GAP = "MONETARY_SEMANTIC_GAP"
    CORRECTION_TARGET_UNRESOLVED = "CORRECTION_TARGET_UNRESOLVED"
    UNREPRESENTED_NEGATION = "UNREPRESENTED_NEGATION"
    UNRESOLVED_REQUIREMENT_CLAUSE = "UNRESOLVED_REQUIREMENT_CLAUSE"


class SemanticCoverageSignals(BaseModel):
    model_config = ConfigDict(extra="forbid")

    monetary_expressions: int = Field(ge=0)
    resolved_constraints: int = Field(ge=0)
    blocking_ambiguities: int = Field(ge=0)


class SemanticCoverageResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    needs_llm: bool
    reasons: list[CoverageReason] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    signals: SemanticCoverageSignals


MONEY_EXPRESSION = re.compile(r"(?:[$€£]\s*\d|\b(?:USD|EUR|GBP)\s+\d)", re.I)
TRADEOFF_LANGUAGE = re.compile(
    r"\b(?:if\s+necessary|okay\s+spending\s+more|"
    r"prioriti[sz]e\b[^.!?;]{0,60}\bover|rather\s+(?:spend|pay)|"
    r"(?:save|spend\s+less)\b[^.!?;]{0,60}\bso\b|"
    r"(?:spend|pay)\s+(?:a\s+little\s+)?(?:more|extra)\b[^.!?;]{0,60}\b(?:if|while)|"
    r"(?:cheaper|simpler)\b[^.!?;]{0,60}\bif|value\b[^.!?;]{0,60}\bover)\b"
    r"|\bstretch\b[^.!?;]{0,40}\bbudget\b[^.!?;]{0,40}\bif\b",
    re.I,
)
LEGACY_MONETARY_TRADEOFF = re.compile(
    r"\b(?:if necessary|okay spending more|rather spend|rather pay)\b", re.I
)
NUMBER = re.compile(r"(?<![\w])(?:[$€£]\s*|(?:USD|EUR|GBP)\s+)?(?P<value>\d[\d,]*)", re.I)
MONEY_CONTEXT = re.compile(
    r"\b(?:budget|budgt|money|spend(?:ing)?|cost|trip|hotel|lodg\w*|ac+om+odation|"
    r"food|dining|restaurants?|transport|transit|flights?|airfare|activities?|attractions?|total)\b",
    re.I,
)
HARD_MONEY_CONTEXT = re.compile(
    r"\b(?:under|below|max(?:imum)?|cap(?:ped)?|ceiling|within|must|should|shud|"
    r"cannot|can't|cant|no\s+more|not\s+more|cost\s+less)\b",
    re.I,
)
CORRECTION_CUE = re.compile(r"\b(?:actually|sorry|make|change|instead|use)\b", re.I)
SOFT_CAP_REJECTION = re.compile(r"\bnot\s+(?:a\s+)?strict\s+cap\b", re.I)
SOFT_MONEY_CONTEXT = re.compile(
    r"\b(?:around|about|roughly|ideally|ideal|flexible|target|if\s+possible)\b", re.I
)
HOTEL_MONEY = re.compile(
    r"(?:[$€£]\s*\d[\d,]*[^.!?;]{0,40}\b(?:hotel|place\s+to\s+stay|lodging|accommodation)\b|"
    r"\b(?:hotel|place\s+to\s+stay|lodging|accommodation)\b[^.!?;]{0,40}[$€£]\s*\d)",
    re.I,
)
SOFT_HOTEL_MONEY = re.compile(
    r"(?:\bhotel\b[^.!?;]{0,30}\b(?:around|about)\b[^.!?;]{0,20}[$€£]\s*\d|"
    r"\b(?:around|about)\b[^.!?;]{0,20}[$€£]\s*\d[^.!?;]{0,30}\bhotel\b)",
    re.I,
)
EXCLUSION_CUE = re.compile(
    r"\b(?:(?:do\s+not|don't)\s+(?:include|need|schedule|care\s+about)|"
    r"(?:please\s+)?exclude|avoid|without|no(?!\s+more\s+than))\b",
    re.I,
)
EXCLUSION_TARGET = re.compile(
    r"\b(?:zoos?|nightlife|luxury\s+hotels?|restaurants?|museums?|parks?|seafood|"
    r"casino|hotel\s+areas?|attractions?|activities?)\b",
    re.I,
)
PREFERENCE_CUE = re.compile(
    r"\b(?:find\s+me\s+(?:zoos?|museums?|parks?)|"
    r"i\s+(?:like|enjoy|prefer|love)\b|i\s+want\s+(?!to\s+spend|\d)|"
    r"(?:public\s+transit)\s+is\s+preferred|i'd\s+rather\s+stay|"
    r"(?:zoos?|museums?|parks?)[^.!?;]{0,50}\bplease|"
    r"(?:quiet|downtown)\s+hotel)\b",
    re.I,
)


class SemanticCoverageAnalyzer:
    def analyze(self, query: str, requirements: TravelRequirements) -> SemanticCoverageResult:
        reasons = []
        evidence = []
        ambiguities = requirements.requirements_v2.ambiguities
        for ambiguity in ambiguities:
            if ambiguity.level != "BLOCKING":
                continue
            if "not supported" in ambiguity.reason:
                continue
            reason = CoverageReason.AMBIGUOUS_SCOPE
            if reason not in reasons:
                reasons.append(reason)
            if ambiguity.source_text not in evidence:
                evidence.append(ambiguity.source_text)
        tradeoff = TRADEOFF_LANGUAGE.search(query) or (
            LEGACY_MONETARY_TRADEOFF.search(query) if MONEY_EXPRESSION.search(query) else None
        )
        if tradeoff:
            reasons.append(CoverageReason.TRADEOFF_LANGUAGE)
            evidence.append(tradeoff.group(0))
        exclusion = unrepresented_exclusion(query)
        if exclusion:
            reasons.append(CoverageReason.UNREPRESENTED_NEGATION)
            evidence.append(exclusion)
        preference = PREFERENCE_CUE.search(query)
        destination_suffix = (
            f" in {requirements.destination.casefold()}" if requirements.destination else None
        )
        if (
            preference
            and not ambiguities
            and (
                not requirements.requirements_v2.preferences
                or (
                    destination_suffix
                    and any(
                        destination_suffix in item.value
                        for item in requirements.requirements_v2.preferences
                    )
                )
            )
        ):
            reasons.append(CoverageReason.UNRESOLVED_REQUIREMENT_CLAUSE)
            evidence.append(preference.group(0))
        soft_hotel_money = SOFT_HOTEL_MONEY.search(query)
        if (
            soft_hotel_money
            and any(
                item.scope.value == "TOTAL_TRIP"
                for item in requirements.requirements_v2.constraints
            )
            and any(
                item.category.value == "HOTEL" for item in requirements.requirements_v2.preferences
            )
        ):
            reasons.append(CoverageReason.UNRESOLVED_REQUIREMENT_CLAUSE)
            evidence.append(soft_hotel_money.group(0))
        money_gaps = unrepresented_hard_money(query, requirements)
        if money_gaps or (
            SOFT_CAP_REJECTION.search(query) and requirements.requirements_v2.constraints
        ):
            reasons.append(CoverageReason.MONETARY_SEMANTIC_GAP)
            evidence.extend(money_gaps or [SOFT_CAP_REJECTION.search(query).group(0)])
        correction_gap = unresolved_correction(query, requirements)
        if correction_gap:
            reasons.append(CoverageReason.CORRECTION_TARGET_UNRESOLVED)
            evidence.append(correction_gap)
        hotel_money = HOTEL_MONEY.search(query)
        if (
            hotel_money
            and not requirements.requirements_v2.constraints
            and not requirements.requirements_v2.preferences
            and not ambiguities
            and not SOFT_MONEY_CONTEXT.search(hotel_money.group(0))
        ):
            reasons.append(CoverageReason.AMBIGUOUS_SCOPE)
            evidence.append(hotel_money.group(0))
        return SemanticCoverageResult(
            needs_llm=bool(reasons),
            reasons=reasons,
            evidence=evidence,
            signals=SemanticCoverageSignals(
                monetary_expressions=len(budget_like_amounts(query)),
                resolved_constraints=len(requirements.requirements_v2.constraints),
                blocking_ambiguities=sum(item.level == "BLOCKING" for item in ambiguities),
            ),
        )


def budget_like_amounts(query: str) -> list[tuple[float, int, int, str]]:
    amounts = []
    for match in NUMBER.finditer(query):
        value = float(match["value"].replace(",", ""))
        if value < 50:
            continue
        start = max(query.rfind(mark, 0, match.start()) for mark in ".!?;") + 1
        ends = [index for mark in ".!?;" if (index := query.find(mark, match.end())) >= 0]
        end = min(ends, default=len(query))
        clause = query[start:end].strip()
        if (
            MONEY_CONTEXT.search(clause)
            and HARD_MONEY_CONTEXT.search(clause)
            and not SOFT_MONEY_CONTEXT.search(clause)
        ):
            amounts.append((value, match.start(), match.end(), clause))
    return amounts


def unrepresented_hard_money(query: str, requirements: TravelRequirements) -> list[str]:
    amounts = budget_like_amounts(query)
    represented = {item.value for item in requirements.requirements_v2.constraints}
    if requirements.budget_amount is not None and requirements.budget_constraint_strength == "HARD":
        represented.add(requirements.budget_amount)
    for ambiguity in requirements.requirements_v2.ambiguities:
        represented.update(
            float(value.replace(",", ""))
            for value in re.findall(r"\b\d[\d,]*\b", ambiguity.source_text)
        )
    gaps = []
    for value, _, end, clause in amounts:
        if value in represented:
            continue
        remainder = query[end:]
        if CORRECTION_CUE.search(remainder):
            later_values = {
                float(match["value"].replace(",", "")) for match in NUMBER.finditer(remainder)
            }
            if later_values.intersection(represented):
                continue
        if clause not in gaps:
            gaps.append(clause)
    return gaps


def unresolved_correction(query: str, requirements: TravelRequirements) -> str | None:
    constraints = requirements.requirements_v2.constraints
    for cue in CORRECTION_CUE.finditer(query):
        end = min(
            [index for mark in ".!?;" if (index := query.find(mark, cue.end())) >= 0],
            default=len(query),
        )
        clause = query[cue.start() : end].strip()
        amounts = [
            match
            for match in NUMBER.finditer(clause)
            if not re.match(r"-?\s*days?\b|\s*stars?\b", clause[match.end() :], re.I)
            and not re.search(r"\bnot\s*$", clause[: match.start()], re.I)
        ]
        if not amounts:
            continue
        amount = amounts[0]
        value = float(amount["value"].replace(",", ""))
        scope = (
            "TOTAL_TRIP"
            if re.search(r"\b(?:trip|total)\b", clause, re.I)
            else "HOTEL_TOTAL"
            if re.search(r"\b(?:hotel|lodging|accommodation)\b", clause, re.I)
            else None
        )
        if scope is not None:
            if not any(item.scope.value == scope and item.value == value for item in constraints):
                return clause
        elif not any(item.value == value for item in constraints):
            return clause
    return None


def unrepresented_exclusion(query: str) -> str | None:
    for clause in re.split(r"[.!?;]", query):
        if EXCLUSION_CUE.search(clause) and EXCLUSION_TARGET.search(clause):
            return clause.strip()
    return None
