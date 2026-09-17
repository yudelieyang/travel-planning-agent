"""Deterministic promotion policy for untrusted semantic proposals."""

import re
from collections.abc import Iterable
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from app.agent.requirements import (
    AmbiguityLevel,
    BudgetConstraint,
    ConstraintExtractorSource,
    ConstraintScope,
    ConstraintStrength,
    PreferenceCategory,
    RequirementAmbiguity,
    SpecificPreference,
    TravelRequirements,
)
from app.agent.semantic_extractor import (
    SemanticExtractionResult,
    SemanticProposalConstraint,
    SemanticProposalScope,
    SemanticProposalStrength,
)
from app.core.budget import BudgetScope


class MergeDecisionCode(StrEnum):
    ADDED_FROM_LLM = "ADDED_FROM_LLM"
    DUPLICATE_CONFIRMED = "DUPLICATE_CONFIRMED"
    DETERMINISTIC_PRESERVED = "DETERMINISTIC_PRESERVED"
    LLM_REJECTED_CONFLICT = "LLM_REJECTED_CONFLICT"
    LLM_REJECTED_UNGROUNDED = "LLM_REJECTED_UNGROUNDED"
    LLM_REJECTED_UNSAFE = "LLM_REJECTED_UNSAFE"
    CORRECTION_SCOPE_QUARANTINED = "CORRECTION_SCOPE_QUARANTINED"
    STALE_VALUE_REMOVED = "STALE_VALUE_REMOVED"
    STALE_PROPOSAL_REJECTED = "STALE_PROPOSAL_REJECTED"
    CORRECTION_REPLACEMENT_REJECTED = "CORRECTION_REPLACEMENT_REJECTED"
    CORRECTION_APPLIED = "CORRECTION_APPLIED"
    UNSUPPORTED_RETAINED = "UNSUPPORTED_RETAINED"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"


class MergeConflictCode(StrEnum):
    EXPLICIT_CONSTRAINT_CONFLICT = "EXPLICIT_CONSTRAINT_CONFLICT"
    HARD_SOFT_CONFLICT = "HARD_SOFT_CONFLICT"
    AMBIGUOUS_SCOPE = "AMBIGUOUS_SCOPE"
    UNSAFE_HARD_PROPOSAL = "UNSAFE_HARD_PROPOSAL"
    UNRESOLVED_CORRECTION = "UNRESOLVED_CORRECTION"
    UNSUPPORTED_SEMANTIC = "UNSUPPORTED_SEMANTIC"


class MergeDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: MergeDecisionCode
    subject: str
    source_text: str | None = None


class MergeConflict(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: MergeConflictCode
    subject: str
    reason: str


class HybridMergeResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requirements: TravelRequirements
    decisions: list[MergeDecision] = Field(default_factory=list)
    conflicts: list[MergeConflict] = Field(default_factory=list)
    requires_clarification: bool = False


_SUPPORTED_SCOPES = {
    SemanticProposalScope.TOTAL_TRIP: ConstraintScope.TOTAL_TRIP,
    SemanticProposalScope.HOTEL_TOTAL: ConstraintScope.HOTEL_TOTAL,
}
_PREFERENCE_FIELDS = {
    PreferenceCategory.ACTIVITY: "interests",
    PreferenceCategory.FOOD: "food_preferences",
    PreferenceCategory.HOTEL: "hotel_preferences",
    PreferenceCategory.TRANSPORT: "transport_preferences",
}


def merge_requirements(
    deterministic: TravelRequirements,
    proposal: SemanticExtractionResult,
    query: str,
    coverage_reasons: Iterable[str] = (),
) -> HybridMergeResult:
    """Return a new canonical requirement set without trusting the proposal by default."""
    requirements = TravelRequirements.model_validate_json(deterministic.model_dump_json())
    decisions: list[MergeDecision] = []
    conflicts: list[MergeConflict] = []
    requires_clarification = False
    reasons = {getattr(reason, "value", str(reason)) for reason in coverage_reasons}

    def decide(code: MergeDecisionCode, subject: str, source_text: str | None = None) -> None:
        decisions.append(MergeDecision(code=code, subject=subject, source_text=source_text))

    def clarify(code: MergeConflictCode, subject: str, reason: str, source_text: str) -> None:
        nonlocal requires_clarification
        conflicts.append(MergeConflict(code=code, subject=subject, reason=reason))
        decide(MergeDecisionCode.CLARIFICATION_REQUIRED, subject, source_text)
        _ensure_blocking_ambiguity(requirements, source_text, reason)
        requires_clarification = True

    if "AMBIGUOUS_SCOPE" in reasons and not _has_any_blocking_ambiguity(requirements):
        clarify(
            MergeConflictCode.AMBIGUOUS_SCOPE,
            "ambiguous monetary scope",
            "A monetary scope remains ambiguous and is not executable.",
            query,
        )
    if "UNREPRESENTED_NEGATION" in reasons:
        clarify(
            MergeConflictCode.UNSUPPORTED_SEMANTIC,
            "negation or exclusion",
            "The exclusion is retained as non-executable semantic intent.",
            query,
        )
    if "TRADEOFF_LANGUAGE" in reasons:
        clarify(
            MergeConflictCode.UNSUPPORTED_SEMANTIC,
            "tradeoff",
            "The conditional tradeoff is retained as non-executable semantic intent.",
            query,
        )

    correction = (
        _correction_context(query, requirements)
        if reasons.intersection({"CORRECTION_TARGET_UNRESOLVED", "AMBIGUOUS_SCOPE"})
        else None
    )
    quarantined_scopes = (
        {correction[0]}
        if correction and correction[0] is not None
        else {item.scope for item in requirements.requirements_v2.constraints}
        if correction
        else set()
    )
    for scope in quarantined_scopes:
        decide(MergeDecisionCode.CORRECTION_SCOPE_QUARANTINED, scope.value, correction[2])
    corrected_item = (
        _apply_correction(requirements, proposal, query, correction, reasons, decisions)
        if correction
        else None
    )
    if correction and corrected_item is None:
        clarify(
            MergeConflictCode.UNRESOLVED_CORRECTION,
            "correction",
            "The correction target or proposed replacement is not safe to apply.",
            correction[2],
        )

    for item in proposal.constraints:
        if item is corrected_item:
            continue
        subject = f"{item.scope} <= {item.value:g} {item.currency} {item.strength}"
        canonical_scope = _SUPPORTED_SCOPES.get(item.scope)
        if canonical_scope in quarantined_scopes:
            decide(MergeDecisionCode.STALE_PROPOSAL_REJECTED, subject, item.source_text)
            continue
        if not _is_grounded(item.source_text, query):
            decide(MergeDecisionCode.LLM_REJECTED_UNGROUNDED, subject, item.source_text)
            continue
        if canonical_scope is None:
            _retain_unsupported(requirements, item, decisions)
            if item.strength == SemanticProposalStrength.HARD:
                requires_clarification = True
                decide(MergeDecisionCode.CLARIFICATION_REQUIRED, subject, item.source_text)
            continue
        existing = next(
            (constraint for constraint in requirements.requirements_v2.constraints if constraint.scope == canonical_scope),
            None,
        )
        if existing is not None:
            if _same_constraint(existing, item):
                decide(MergeDecisionCode.DUPLICATE_CONFIRMED, subject, item.source_text)
            else:
                decide(MergeDecisionCode.DETERMINISTIC_PRESERVED, subject, item.source_text)
                clarify(
                    MergeConflictCode.EXPLICIT_CONSTRAINT_CONFLICT,
                    subject,
                    "Explicit deterministic budget differs from the semantic proposal.",
                    item.source_text,
                )
            continue
        if _has_soft_budget_preference(requirements, canonical_scope):
            decide(MergeDecisionCode.DETERMINISTIC_PRESERVED, subject, item.source_text)
            clarify(
                MergeConflictCode.HARD_SOFT_CONFLICT,
                subject,
                "A deterministic soft budget preference cannot be upgraded to a hard constraint.",
                item.source_text,
            )
            continue
        if item.strength != SemanticProposalStrength.HARD:
            decide(MergeDecisionCode.DETERMINISTIC_PRESERVED, subject, item.source_text)
            continue
        if not _hard_proposal_is_safe(item, reasons):
            decide(MergeDecisionCode.LLM_REJECTED_UNSAFE, subject, item.source_text)
            clarify(
                MergeConflictCode.UNSAFE_HARD_PROPOSAL,
                subject,
                "The source does not unambiguously justify this executable hard constraint.",
                item.source_text,
            )
            continue
        requirements.requirements_v2.constraints.append(
            BudgetConstraint(
                scope=canonical_scope,
                value=item.value,
                currency=item.currency,
                source_text=item.source_text,
                extractor_source=ConstraintExtractorSource.MERGED,
            )
        )
        decide(MergeDecisionCode.ADDED_FROM_LLM, subject, item.source_text)

    for item in proposal.preferences:
        subject = f"{item.category}: {item.value}"
        if not _is_grounded(item.source_text, query):
            decide(MergeDecisionCode.LLM_REJECTED_UNGROUNDED, subject, item.source_text)
        elif not _preference_is_safe(item, requirements, reasons):
            decide(MergeDecisionCode.LLM_REJECTED_UNSAFE, subject, item.source_text)
        elif any(
            preference.category == item.category and preference.value.casefold() == item.value.casefold()
            for preference in requirements.requirements_v2.preferences
        ):
            decide(MergeDecisionCode.DUPLICATE_CONFIRMED, subject, item.source_text)
        else:
            preference = SpecificPreference(category=item.category, value=item.value)
            requirements.requirements_v2.preferences.append(preference)
            requirements.specific_preferences.append(preference)
            field = _PREFERENCE_FIELDS.get(item.category)
            if field is not None and item.value not in getattr(requirements, field):
                getattr(requirements, field).append(item.value)
            if item.category == PreferenceCategory.FOOD and "food" not in requirements.interests:
                requirements.interests.append("food")
            decide(MergeDecisionCode.ADDED_FROM_LLM, subject, item.source_text)

    for item in proposal.ambiguities:
        subject = item.reason
        if not _is_grounded(item.source_text, query):
            decide(MergeDecisionCode.LLM_REJECTED_UNGROUNDED, subject, item.source_text)
        elif reasons.intersection(
            {"AMBIGUOUS_SCOPE", "UNREPRESENTED_NEGATION", "TRADEOFF_LANGUAGE"}
        ) and item.level != AmbiguityLevel.BLOCKING:
            decide(MergeDecisionCode.LLM_REJECTED_UNSAFE, subject, item.source_text)
        elif not any(
            ambiguity.source_text == item.source_text and ambiguity.reason == item.reason
            for ambiguity in requirements.requirements_v2.ambiguities
        ):
            requirements.requirements_v2.ambiguities.append(
                RequirementAmbiguity(level=item.level, source_text=item.source_text, reason=item.reason)
            )
            decide(MergeDecisionCode.ADDED_FROM_LLM, subject, item.source_text)
            requires_clarification |= item.level == AmbiguityLevel.BLOCKING

    for objective in proposal.objectives:
        # The Phase F objective schema intentionally has no source text, so it cannot pass grounding.
        decide(MergeDecisionCode.LLM_REJECTED_UNGROUNDED, objective.value)

    return HybridMergeResult(
        requirements=TravelRequirements.model_validate_json(requirements.model_dump_json()),
        decisions=decisions,
        conflicts=conflicts,
        requires_clarification=requires_clarification or _has_any_blocking_ambiguity(requirements),
    )


def _is_grounded(source_text: str, query: str) -> bool:
    source, original = normalize(source_text), normalize(query)
    return bool(source) and source in original


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.casefold())


def _has_any_blocking_ambiguity(requirements: TravelRequirements) -> bool:
    return any(
        ambiguity.level == AmbiguityLevel.BLOCKING
        for ambiguity in requirements.requirements_v2.ambiguities
    )


def _ensure_blocking_ambiguity(
    requirements: TravelRequirements, source_text: str, reason: str
) -> None:
    if any(
        ambiguity.level == AmbiguityLevel.BLOCKING
        and normalize(ambiguity.source_text) == normalize(source_text)
        and ambiguity.reason == reason
        for ambiguity in requirements.requirements_v2.ambiguities
    ):
        return
    requirements.requirements_v2.ambiguities.append(
        RequirementAmbiguity(
            level=AmbiguityLevel.BLOCKING,
            source_text=source_text,
            reason=reason,
        )
    )


def _correction_context(
    query: str, requirements: TravelRequirements
) -> tuple[ConstraintScope | None, float | None, str] | None:
    cues = list(
        re.finditer(r"\b(?:actually|sorry|make|change|adjust|instead|use)\b", query, re.I)
    )
    if not cues:
        return None
    for cue in reversed(cues):
        end = min(
            [index for mark in ".!?;" if (index := query.find(mark, cue.start())) >= 0],
            default=len(query),
        )
        clause = query[cue.start() : end].strip()
        if normalize(clause) == "instead":
            continue
        amount = re.search(
            r"(?:[$€£]\s*|\b(?:USD|EUR|GBP)\s+)?(?P<value>\d[\d,]*)",
            clause,
            re.I,
        )
        if re.search(r"\b(?:hotel|lodging|accommodation)\b", clause, re.I):
            scope = ConstraintScope.HOTEL_TOTAL
        elif re.search(r"\b(?:trip|total)\b", clause, re.I):
            scope = ConstraintScope.TOTAL_TRIP
        else:
            scopes = {item.scope for item in requirements.requirements_v2.constraints}
            scope = scopes.pop() if len(scopes) == 1 else None
        value = float(amount["value"].replace(",", "")) if amount else None
        return scope, value, clause
    return None


def _apply_correction(
    requirements: TravelRequirements,
    proposal: SemanticExtractionResult,
    query: str,
    correction: tuple[ConstraintScope | None, float | None, str],
    coverage_reasons: set[str],
    decisions: list[MergeDecision],
) -> SemanticProposalConstraint | None:
    scope, value, clause = correction
    existing = list(requirements.requirements_v2.constraints)
    stale_scopes = {scope} if scope is not None else {item.scope for item in existing}
    stale = [
        item
        for item in existing
        if item.scope in stale_scopes
        or (
            item.source_text is not None
            and (
                _is_grounded(item.source_text, clause)
                or _is_grounded(clause, item.source_text)
            )
        )
    ]
    clause_start = query.casefold().rfind(clause.casefold())
    prior_query = query[:clause_start] if clause_start >= 0 else query
    inherited_hard = bool(
        scope is not None
        and (
            any(item.scope == scope for item in existing)
            or (
                _source_supports_scope(prior_query, scope)
                and _has_hard_cap_language(prior_query)
            )
        )
    )
    inherited_source = f"{prior_query} {clause}".strip()
    candidates = [
        item
        for item in proposal.constraints
        if scope is not None
        and value is not None
        and _SUPPORTED_SCOPES.get(item.scope) == scope
        and item.value == value
        and item.strength == SemanticProposalStrength.HARD
        and (
            _is_grounded(item.source_text, clause)
            or _is_grounded(clause, item.source_text)
        )
        and inherited_hard
        and _hard_proposal_is_safe(
            item.model_copy(update={"source_text": inherited_source}), coverage_reasons
        )
    ]
    for item in stale:
        requirements.requirements_v2.constraints.remove(item)
        decisions.append(
            MergeDecision(
                code=MergeDecisionCode.STALE_VALUE_REMOVED,
                subject=f"{item.scope} <= {item.value:g} {item.currency} HARD",
                source_text=item.source_text,
            )
        )
    if any(item.scope == ConstraintScope.TOTAL_TRIP for item in stale):
        requirements.budget_amount = None
        requirements.budget_scope = BudgetScope.UNKNOWN
        requirements.budget_constraint_strength = ConstraintStrength.UNSPECIFIED
    if len(candidates) != 1:
        decisions.append(
            MergeDecision(
                code=MergeDecisionCode.CORRECTION_REPLACEMENT_REJECTED,
                subject=scope.value if scope is not None else "ambiguous correction scope",
                source_text=clause,
            )
        )
        return None
    item = candidates[0]
    requirements.requirements_v2.ambiguities = [
        ambiguity
        for ambiguity in requirements.requirements_v2.ambiguities
        if not (
            _is_grounded(ambiguity.source_text, clause)
            or _is_grounded(clause, ambiguity.source_text)
        )
    ]
    requirements.requirements_v2.constraints.append(
        BudgetConstraint(
            scope=scope,
            value=item.value,
            currency=item.currency,
            source_text=item.source_text,
            extractor_source=ConstraintExtractorSource.MERGED,
        )
    )
    decisions.append(
        MergeDecision(
            code=MergeDecisionCode.CORRECTION_APPLIED,
            subject=f"{scope} <= {item.value:g} {item.currency} HARD",
            source_text=item.source_text,
        )
    )
    return item


def _proposal_amount_is_explicit(item: SemanticProposalConstraint) -> bool:
    values = {
        float(value.replace(",", ""))
        for value in re.findall(r"\d[\d,]*(?:\.\d+)?", item.source_text)
    }
    return item.value in values


def _has_hard_cap_language(source_text: str) -> bool:
    return bool(
        re.search(
            r"\b(?:under|below|at\s+most|max(?:imum)?|cap(?:ped)?|ceiling|must|cannot|can't|"
            r"cant\s+above|no\s+more\s+than|not\s+more\s+than|should\s+not\s+more\s+th[ae]n|"
            r"must\s+not\s+exceed|cannot\s+exceed)\b",
            source_text,
            re.I,
        )
    )


def _source_supports_scope(source_text: str, scope: ConstraintScope) -> bool:
    if scope == ConstraintScope.TOTAL_TRIP:
        return bool(
            re.search(
                r"\b(?:(?:whole|entire|full|all|total)\s+trip|trip\s+(?:total|budg(?:et|t)|ceiling|max)|"
                r"trip\b[^.!?;]{0,25}\b(?:under|max)|"
                r"total\s+(?:trip|cost)|(?:the\s+)?total\s+is\s+(?:capped|limited)|overall)\b",
                source_text,
                re.I,
            )
        )
    return bool(
        re.search(r"\b(?:hotel|lodging|ac+om+odation)\b", source_text, re.I)
        and re.search(
            r"\b(?:total|whole\s+trip|entire\s+trip|full\s+trip|all\s+(?:lodging|hotel)|combined)\b",
            source_text,
            re.I,
        )
    )


def _hard_proposal_is_safe(item: SemanticProposalConstraint, coverage_reasons: set[str]) -> bool:
    scope = _SUPPORTED_SCOPES.get(item.scope)
    if scope is None:
        return False
    return (
        _proposal_amount_is_explicit(item)
        and item.currency == "USD"
        and _has_hard_cap_language(item.source_text)
        and _source_supports_scope(item.source_text, scope)
        and ("AMBIGUOUS_SCOPE" not in coverage_reasons or _source_supports_scope(item.source_text, scope))
    )


def _preference_is_safe(
    item, requirements: TravelRequirements, coverage_reasons: set[str]
) -> bool:
    if "TRADEOFF_LANGUAGE" in coverage_reasons:
        return False
    if re.search(
        r"\b(?:do\s+not|don't|avoid|exclude|without|no(?!\s+more\s+than))\b",
        item.source_text,
        re.I,
    ):
        return False
    if item.category == PreferenceCategory.UNSPECIFIED:
        return False
    if item.category != PreferenceCategory.HOTEL:
        return True
    return bool(
        re.search(
            r"\b(?:downtown|quiet|luxury|boutique|budget|better|location|room|quality|star|pool|"
            r"accessible|family|business|resort|hostel)\b",
            item.value,
            re.I,
        )
    )


def _same_constraint(existing: BudgetConstraint, proposed: SemanticProposalConstraint) -> bool:
    return (
        existing.value == proposed.value
        and existing.currency == proposed.currency
        and existing.strength.value == proposed.strength.value
    )


def _has_soft_budget_preference(requirements: TravelRequirements, scope: ConstraintScope) -> bool:
    category = PreferenceCategory.HOTEL if scope == ConstraintScope.HOTEL_TOTAL else None
    return category is not None and any(
        preference.category == category and re.search(r"\b(?:around|about)\s+[a-z]*\s*\d", preference.value, re.I)
        for preference in requirements.requirements_v2.preferences
    )


def _retain_unsupported(
    requirements: TravelRequirements,
    item: SemanticProposalConstraint,
    decisions: list[MergeDecision],
) -> None:
    subject = f"{item.scope} <= {item.value:g} {item.currency} {item.strength}"
    reason = f"{subject} is not supported for planning, validation, or repair."
    if not any(ambiguity.reason == reason for ambiguity in requirements.requirements_v2.ambiguities):
        requirements.requirements_v2.ambiguities.append(
            RequirementAmbiguity(
                level=AmbiguityLevel.BLOCKING if item.strength == SemanticProposalStrength.HARD else AmbiguityLevel.ASSUMABLE,
                source_text=item.source_text,
                reason=reason,
            )
        )
    decisions.append(
        MergeDecision(
            code=MergeDecisionCode.UNSUPPORTED_RETAINED,
            subject=subject,
            source_text=item.source_text,
        )
    )
