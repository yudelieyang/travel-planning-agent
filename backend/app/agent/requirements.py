"""Explicit requirements and a deliberately limited, offline English parser."""

import re
from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.budget import BudgetScope
from app.tools.candidate_data import city_at_start, resolve_city


class ConstraintStrength(StrEnum):
    UNSPECIFIED = "UNSPECIFIED"
    HARD = "HARD"
    SOFT = "SOFT"


class ConstraintKind(StrEnum):
    BUDGET = "BUDGET"


class ConstraintScope(StrEnum):
    TOTAL_TRIP = "TOTAL_TRIP"
    HOTEL_TOTAL = "HOTEL_TOTAL"


class ConstraintOperator(StrEnum):
    LTE = "LTE"


class ConstraintExtractorSource(StrEnum):
    DETERMINISTIC = "deterministic"
    LLM = "llm"
    MERGED = "merged"
    LEGACY_PROJECTION = "legacy_projection"


class AmbiguityLevel(StrEnum):
    RESOLVED = "RESOLVED"
    ASSUMABLE = "ASSUMABLE"
    BLOCKING = "BLOCKING"


class OptimizationObjective(StrEnum):
    MAXIMIZE_BUDGET_UTILIZATION = "maximize_budget_utilization"


class PreferenceCategory(StrEnum):
    ACTIVITY = "ACTIVITY"
    FOOD = "FOOD"
    HOTEL = "HOTEL"
    TRANSPORT = "TRANSPORT"
    UNSPECIFIED = "UNSPECIFIED"


class SpecificPreference(BaseModel):
    category: PreferenceCategory
    value: str = Field(min_length=1, max_length=100)


class BudgetConstraint(BaseModel):
    """A small, executable hard-budget contract with extraction provenance."""

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    kind: ConstraintKind = ConstraintKind.BUDGET
    scope: ConstraintScope
    operator: ConstraintOperator = ConstraintOperator.LTE
    value: float = Field(ge=0)
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    strength: ConstraintStrength = ConstraintStrength.HARD
    source_text: str | None = Field(default=None, min_length=1, max_length=500)
    extractor_source: ConstraintExtractorSource = ConstraintExtractorSource.DETERMINISTIC
    confidence: float = Field(default=1.0, ge=0, le=1)

    @model_validator(mode="after")
    def validate_hard_budget_contract(self):
        if self.strength != ConstraintStrength.HARD:
            raise ValueError("Canonical budget constraints must be hard constraints")
        return self


class RequirementAmbiguity(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    level: AmbiguityLevel
    source_text: str = Field(min_length=1, max_length=500)
    reason: str = Field(min_length=1, max_length=200)


class RequirementsV2(BaseModel):
    """Canonical semantic collections; flat fields remain compatibility projections."""

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    constraints: list[BudgetConstraint] = Field(default_factory=list)
    preferences: list[SpecificPreference] = Field(default_factory=list)
    objectives: list[OptimizationObjective] = Field(default_factory=list)
    ambiguities: list[RequirementAmbiguity] = Field(default_factory=list)

    @model_validator(mode="after")
    def reject_duplicate_budget_scopes(self):
        scopes = [constraint.scope for constraint in self.constraints]
        if len(scopes) != len(set(scopes)):
            raise ValueError("Only one canonical budget constraint is allowed per scope")
        return self


class TravelRequirements(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    destination: str | None = None
    origin: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    duration_days: int | None = Field(default=None, ge=1, le=30)
    travelers: int | None = Field(default=None, ge=1, le=20)
    budget_amount: float | None = Field(default=None, ge=0)
    budget_scope: BudgetScope = BudgetScope.UNKNOWN
    budget_constraint_strength: ConstraintStrength = ConstraintStrength.UNSPECIFIED
    objective: OptimizationObjective | None = None
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    interests: list[str] = Field(default_factory=list)
    hotel_preferences: list[str] = Field(default_factory=list)
    food_preferences: list[str] = Field(default_factory=list)
    transport_preferences: list[str] = Field(default_factory=list)
    specific_preferences: list[SpecificPreference] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    requirements_v2: RequirementsV2 = Field(default_factory=RequirementsV2)

    @field_validator("destination", "origin")
    @classmethod
    def normalize_place(cls, value: str | None) -> str | None:
        if not value or not value.strip():
            return None
        value = value.strip()
        city = resolve_city(value)
        return city.city if city is not None else value

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date:
            days = (self.end_date - self.start_date).days + 1
            if not 1 <= days <= 30:
                raise ValueError("Date range must cover 1 to 30 days, inclusive")
            if self.duration_days is not None and self.duration_days != days:
                raise ValueError("Duration conflicts with the inclusive date range")
        return self

    @model_validator(mode="after")
    def project_canonical_requirements_to_legacy_fields(self):
        """Keep legacy callers on the total-trip view while V2 retains every scope."""
        if not self.requirements_v2.constraints and (
            self.budget_amount is not None
            and self.budget_scope == BudgetScope.TOTAL_TRIP
            and self.budget_constraint_strength == ConstraintStrength.HARD
        ):
            self.requirements_v2.constraints = [
                BudgetConstraint(
                    scope=ConstraintScope.TOTAL_TRIP,
                    value=self.budget_amount,
                    currency=self.currency,
                    source_text=None,
                    extractor_source=ConstraintExtractorSource.LEGACY_PROJECTION,
                )
            ]
        total_trip = next(
            (
                constraint
                for constraint in self.requirements_v2.constraints
                if constraint.scope == ConstraintScope.TOTAL_TRIP
            ),
            None,
        )
        if total_trip is not None:
            self.budget_amount = total_trip.value
            self.budget_scope = BudgetScope.TOTAL_TRIP
            self.budget_constraint_strength = total_trip.strength
            self.currency = total_trip.currency
        if not self.requirements_v2.preferences and self.specific_preferences:
            self.requirements_v2.preferences = list(self.specific_preferences)
        if not self.requirements_v2.objectives and self.objective is not None:
            self.requirements_v2.objectives = [self.objective]
        return self

    @property
    def trip_days(self) -> int | None:
        if self.duration_days is not None:
            return self.duration_days
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return None


class RequirementStatus(StrEnum):
    SUFFICIENT = "SUFFICIENT"
    INSUFFICIENT = "INSUFFICIENT"


class RequirementAssessment(BaseModel):
    status: RequirementStatus
    missing_fields: list[str] = Field(default_factory=list)


def assess_requirements(requirements: TravelRequirements) -> RequirementAssessment:
    missing = []
    if not requirements.destination:
        missing.append("destination")
    if requirements.trip_days is None:
        missing.append("duration")
    return RequirementAssessment(
        status=RequirementStatus.INSUFFICIENT if missing else RequirementStatus.SUFFICIENT,
        missing_fields=missing,
    )


def parse_requirements(query: str) -> TravelRequirements:
    """Recognize documented patterns; never fill missing destination/duration/party size."""
    query = " ".join(query.replace("’", "'").replace("\n", ";").split())
    query = re.sub(r"\b(whole|entire|full)-trip\b", r"\1 trip", query, flags=re.I)
    query = re.sub(r"\bmore\s+then\b", "more than", query, flags=re.I)
    query = re.sub(r"\b([A-Za-z])\.([A-Za-z])\.", r"\1\2", query)
    query = re.sub(r"\b([A-Za-z][A-Za-z ]*),\s*([A-Z]{2})\b", r"\1 \2", query)
    values = {}
    place = re.search(
        r"\b(?:to|in|visit)\s+([A-Za-z][A-Za-z ]*?)"
        r"(?=\s+(?:under|for|with|from|on|starting|between|around|but|budget)\b|[.,!?;]|$)",
        query,
        re.I,
    )
    if place:
        values["destination"] = place[1].strip()
        if " in " in values["destination"].casefold():
            values["destination"] = values["destination"].rsplit(" in ", 1)[-1].strip()
    else:
        # Shorthand is fixture-backed; no arbitrary adjective becomes a city.
        short_match = city_at_start(query)
        if short_match:
            short_city, alias_length = short_match
            values["destination"] = short_city.city
            if re.match(r"\s+or\b", query[alias_length:], re.I):
                values["destination"] = None
                values["constraints"] = ["ambiguous destination"]
        if "destination" not in values:
            trip_place = re.search(
                r"\b(?:\d+|" + NUMBER + r")\s*-\s*days?\s+"
                r"(?P<place>[A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]*)*)\s+trip\b",
                query,
            )
            if trip_place:
                values["destination"] = trip_place["place"]
    destination = values.get("destination")
    if destination and re.search(r"\bor\b", destination, re.I):
        values["destination"] = None
        values["constraints"] = ["ambiguous destination"]
    elif destination and re.match(
        r"(?:somewhere|anywhere|rent|eat|stay|book)\b", destination, re.I
    ):
        values["destination"] = None
    origin = re.search(r"\bfrom\s+([A-Za-z][A-Za-z ]*?)\s+to\b", query, re.I)
    if origin:
        values["origin"] = origin[1].strip()
    duration = re.search(rf"(?<![\w.])({NUMBER})\s*[- ]\s*days?\b", query, re.I)
    if duration:
        values["duration_days"] = number_value(duration[1])
    travelers = re.search(
        rf"(?<![\w.])({NUMBER})\s+(?:travelers?|people|persons?|adults?)\b", query, re.I
    )
    if not travelers:
        travelers = re.search(rf"\bfamily of\s+({NUMBER})\b", query, re.I)
    if not travelers:
        travelers = re.search(
            rf"\bfor\s+({NUMBER})(?=\s*(?:[.,;!?]|$|under\b|with\b))", query, re.I
        )
    if travelers:
        values["travelers"] = number_value(travelers[1])
    elif re.search(r"\b(?:traveling|travelling) alone\b", query, re.I):
        values["travelers"] = 1
    elif re.search(r"\bjust me\b", query, re.I):
        values["travelers"] = 1
    elif re.search(r"\bme and my partner\b", query, re.I):
        values["travelers"] = 2
    dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", query)
    if len(dates) > 2:
        raise ValueError("Provide at most a start and an end date")
    if dates:
        values["start_date"] = date.fromisoformat(dates[0])
    if len(dates) == 2:
        values["end_date"] = date.fromisoformat(dates[1])
    budget_matches = recognized_money_expressions(query)
    budget_constraints, ambiguities = extract_budget_constraints(query, budget_matches)
    if budget_constraints or ambiguities:
        values["requirements_v2"] = RequirementsV2(
            constraints=budget_constraints,
            ambiguities=ambiguities,
        )
    legacy_amount = legacy_budget_projection_match(query, budget_matches)
    if legacy_amount is not None and not budget_constraints:
        # Preserve the old, deliberately conservative projection for non-hard budgets.
        amount = legacy_amount
        multiplier = 1000 if amount["multiplier"] else 1
        values["budget_amount"] = float(amount["amount"].replace(",", "")) * multiplier
        prefix, scope_text = budget_context(query, amount)
        intro = (amount["intro"] or "").casefold()
        if re.match(r"(?:per (?:person|traveler)|each)\b", scope_text, re.I):
            values["budget_scope"] = BudgetScope.PER_PERSON
        elif re.match(
            r"(?:total|(?:for|on) (?:the )?(?:(?:whole|entire) )?trip)\b",
            scope_text,
            re.I,
        ) or re.search(
            r"\b(?:total budget|whole trip|entire trip)\b", f"{prefix} {intro}", re.I
        ):
            values["budget_scope"] = BudgetScope.TOTAL_TRIP
        strength = budget_strength(f"{prefix} {intro}")
        if strength == ConstraintStrength.HARD and budget_strength(
            f"{prefix} {intro} {scope_text}"
        ) == ConstraintStrength.SOFT:
            strength = ConstraintStrength.SOFT
        if strength == ConstraintStrength.SOFT:
            values.setdefault("constraints", []).append("approximate budget")
        if strength != ConstraintStrength.UNSPECIFIED:
            values["budget_constraint_strength"] = strength
        values["currency"] = budget_currency(amount)
    elif not budget_matches and invalid_budget_value(query):
        raise ValueError("Budget amount must be numeric")
    if re.search(
        r"\bspend\s+as\s+much\b[^.!?;]{0,80}\bbudget\s+as\s+(?:reasonably\s+)?possible\b",
        query,
        re.I,
    ):
        values["objective"] = OptimizationObjective.MAXIMIZE_BUDGET_UTILIZATION
    vocabulary = {
        "interests": ["museums", "food", "parks", "history", "art"],
        "hotel_preferences": ["quiet", "central", "budget", "luxury"],
        "food_preferences": ["vegetarian", "vegan", "seafood"],
        "transport_preferences": ["walking", "public transit", "taxi"],
    }
    clauses = re.split(r"[.!?;]|\b(?:but|however)\b", query.lower())
    constraints = values.setdefault("constraints", [])
    for field, terms in vocabulary.items():
        values[field] = []
        for term in terms:
            for clause in clauses:
                match = re.search(r"\b" + re.escape(term) + r"\b", clause)
                if not match or (term == "budget" and not re.search(r"budget hotels?", clause)):
                    continue
                if term == "walking" and re.search(r"\b(?:city|urban|neighborhood)\s+walking\b", clause):
                    continue
                if re.search(NEGATOR, clause[: match.start()]):
                    constraints.append("no walking" if term == "walking" else "avoid " + term)
                elif term not in values[field]:
                    values[field].append(term)
    for clause in clauses:
        for term, label in NEGATIVE_TERMS.items():
            match = re.search(term, clause)
            if match and re.search(NEGATOR, clause[: match.start()]):
                constraints.append(label)
        if re.search(r"\bwheelchair\b", clause):
            constraints.append("wheelchair")
        must = re.search(r"\bmust\s+.+", clause)
        if must and not any(amount.group(0) in clause for amount in budget_matches):
            constraints.append(must[0].strip())
        if re.search(r"\b(?:cheap|affordable)\b", clause):
            constraints.append(clause.strip())
    specifics = extract_specific_preferences(query) + extract_budget_preferences(query, budget_matches)
    values["specific_preferences"] = specifics
    for preference in specifics:
        if preference.category == PreferenceCategory.FOOD:
            if preference.value not in values["food_preferences"]:
                values["food_preferences"].append(preference.value)
            if "food" not in values["interests"]:
                values["interests"].append("food")
        elif preference.category == PreferenceCategory.ACTIVITY:
            if preference.value not in values["interests"]:
                values["interests"].append(preference.value)
        elif preference.category == PreferenceCategory.TRANSPORT:
            if preference.value not in values["transport_preferences"]:
                values["transport_preferences"].append(preference.value)
        elif preference.category == PreferenceCategory.HOTEL:
            if preference.value not in values["hotel_preferences"]:
                values["hotel_preferences"].append(preference.value)
    values["constraints"] = list(dict.fromkeys(constraints))
    return TravelRequirements(**values)


NUMBER_WORDS = dict(
    zip(
        "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split(),
        range(1, 21),
        strict=True,
    )
)
NUMBER = r"-?\d+|" + "|".join(NUMBER_WORDS)
NEGATOR = r"\b(?:don't|do not|no|not|avoid|without|never)\b"
NEGATIVE_TERMS = {
    r"\bnightlife\b": "no nightlife",
    r"\bmeat\b": "no meat",
    r"\b(?:rent a car|rental cars?)\b": "no rental car",
    r"\bexpensive restaurants?\b": "avoid expensive restaurants",
}
BUDGET_PATTERN = re.compile(
    r"(?:(?P<intro>under|below|up to|around|max(?:imum)?|at most|no more than|don't spend more than|"
    r"(?:don't\s+let\s+(?:the\s+)?(?:total|trip|whole\s+trip)\s+go\s+over)|"
    r"(?:cap\s+(?:the\s+)?(?:whole\s+)?trip\s+at)|"
    r"(?:my\s+)?(?:total\s+)?budget(?:\s+(?:of|is))?)\s*)?"
    r"(?:(?P<code>USD|EUR|GBP)\s*|(?P<symbol>[$€£])\s*)?"
    r"(?P<amount>-?\d(?:[\d,]*\d)?(?:\.\d+)?)(?P<multiplier>[kK])?\s*"
    r"(?P<currency>USD|EUR|GBP|dollars?|euros?|pounds?)?",
    re.I,
)
PREFERENCE_PATTERN = re.compile(
    r"\bi\s+(?:also\s+)?(?:like|enjoy|prefer|love|need)\s+(?P<values>[^.!?;]+)", re.I
)
PREFERENCE_CONNECTOR = re.compile(r"\s*(?:,|\b(?:and|but)\b)\s*", re.I)
PREFERENCE_PREFIX = re.compile(
    r"^(?:(?:i\s+)?(?:also\s+)?(?:like|enjoy|prefer|love|need)\s+|also\s+)", re.I
)
BUDGET_INTENT = re.compile(
    r"\b(?:budget|spending\s+limit|spend|afford|under|up\s+to|max(?:imum)?|"
    r"at\s+most|no\s+more\s+than|around|about)\b",
    re.I,
)
BUDGET_HARD = re.compile(
    r"\b(?:under|below|up\s+to|max(?:imum)?|at\s+most|no\s+more\s+than|"
    r"(?:do not|don't)\s+spend\s+more\s+than|spending\s+limit|"
    r"(?:do\s+not|don't)\s+let\s+(?:the\s+)?(?:total|(?:total\s+)?trip)\s+go\s+over|"
    r"cap\s+(?:the\s+)?(?:whole\s+)?trip\s+at|(?:total\s+)?budget|"
    r"(?:must|should)\s+(?:not\s+)?(?:exceed|be\s+more\s+than)|"
    r"cannot\s+(?:exceed|go\s+above)|(?:absolute\s+)?ceiling|"
    r"(?:capped?|cap)(?:\s+is)?(?:\s+at)?|\bwithin\b|\bonly\s+have\b)\b",
    re.I,
)
BUDGET_SOFT = re.compile(
    r"\b(?:around|about|roughly|near|ideally|ideal|if\s+possible|would\s+(?:like|be\s+ideal)|flexible)\b",
    re.I,
)
GENERIC_PREFERENCE_TERMS = frozenset(
    {
        "museums",
        "food",
        "parks",
        "history",
        "art",
        "quiet",
        "central",
        "budget",
        "luxury",
        "vegetarian",
        "vegan",
        "seafood",
        "walking",
        "public transit",
        "taxi",
    }
)


def invalid_budget_value(query: str) -> bool:
    match = re.search(
        r"\b(?:maximum\s+|total\s+|my\s+)?budget\s*(?:is|=|of)?\s*(?P<value>[A-Za-z]+)\b",
        query,
        re.I,
    )
    return bool(match and match["value"].casefold() not in {"hotel", "hotels"})


def budget_context(query: str, amount: re.Match) -> tuple[str, str]:
    """Return text around one amount, bounded to its sentence-like clause."""
    boundaries = list(
        re.finditer(
            r"(?:\b(?:but|however)\b|\b(?:while|and|with)\s+(?:the\s+|a\s+)?(?="
            r"(?:hotel|hotels|lodging|accommodation|food|transport|flight|attractions?|"
            r"(?:whole|entire|full)\s+trip|total)\b)|"
            r"\band\s+(?:would|i|spend|keep)\b|,\s*(?:hotel|hotels|lodging|accommodation|"
            r"food|transport|flight|attractions?|while\s+(?:the\s+)?(?:whole|entire|full)\s+trip|"
            r"with\s+(?:a\s+|the\s+)?(?:hotel|lodging|accommodation))\b)",
            query,
            re.I,
        )
    )
    starts = [query.rfind(mark, 0, amount.start()) for mark in ".!?;"]
    starts += [
        match.start() if match.group().lstrip().startswith(",") else match.end() - 1
        for match in boundaries
        if match.start() < amount.start()
    ]
    start = max(starts, default=-1) + 1
    ends = [index for mark in ".!?;" if (index := query.find(mark, amount.end())) >= 0]
    ends += [match.start() for match in boundaries if match.start() >= amount.end()]
    end = min(ends, default=len(query))
    return query[start : amount.start()].strip(), query[amount.end() : end].strip()


def has_budget_intent(query: str, amount: re.Match) -> bool:
    prefix, suffix = budget_context(query, amount)
    matches = list(BUDGET_INTENT.finditer(prefix))
    if matches and not re.search(r"\d", prefix[matches[-1].end() :]):
        return True
    have = list(re.finditer(r"\bhave\b", prefix, re.I))
    return bool(
        have
        and not re.search(r"\d", prefix[have[-1].end() :])
        and re.match(r"(?:for|on) (?:the )?trip\b", suffix, re.I)
    )


def recognized_money_expressions(query: str) -> list[re.Match]:
    return [
        amount
        for amount in BUDGET_PATTERN.finditer(query)
        if any(amount[key] for key in ("intro", "code", "symbol", "currency"))
        or has_budget_intent(query, amount)
    ]


def extract_budget_constraints(
    query: str, amounts: list[re.Match]
) -> tuple[list[BudgetConstraint], list[RequirementAmbiguity]]:
    candidates = []
    ambiguities = []
    previous_scope: ConstraintScope | None = None
    previous_amount_end: int | None = None
    for amount in amounts:
        created_constraint = False
        prefix, suffix = budget_context(query, amount)
        source_text = f"{prefix} {amount.group(0)} {suffix}".strip()
        scope = monetary_scope(prefix, suffix, amount["intro"] or "")
        correction = previous_amount_end is not None and is_bounded_scope_correction(
            query[previous_amount_end : amount.start()]
        )
        inherited_correction = scope is None and previous_scope is not None and correction
        if inherited_correction:
            scope = previous_scope
        strength = budget_strength(f"{prefix} {amount['intro'] or ''} {suffix}")
        if scope == ConstraintScope.TOTAL_TRIP and re.search(r"\bcan't\s+go\s+above\b", prefix, re.I):
            strength = ConstraintStrength.HARD
        if correction and strength == ConstraintStrength.UNSPECIFIED:
            strength = ConstraintStrength.HARD
        value = float(amount["amount"].replace(",", "")) * (1000 if amount["multiplier"] else 1)
        unsupported_scope = unsupported_money_scope(prefix, suffix)
        if scope == ConstraintScope.HOTEL_TOTAL and ambiguous_hotel_budget_phrase(
            prefix, amount["intro"] or "", suffix
        ):
            ambiguities.append(
                RequirementAmbiguity(
                    level=AmbiguityLevel.BLOCKING,
                    source_text=source_text,
                    reason="Hotel budget does not specify a hard limit or a nightly/total policy",
                )
            )
        elif scope is not None and strength == ConstraintStrength.HARD:
            candidates.append(
                BudgetConstraint(
                    scope=scope,
                    value=value,
                    currency=budget_currency(amount),
                    source_text=source_text,
                )
            )
            previous_scope = scope
            created_constraint = True
        elif unsupported_scope is not None:
            ambiguities.append(
                RequirementAmbiguity(
                    level=AmbiguityLevel.BLOCKING if strength == ConstraintStrength.HARD else AmbiguityLevel.ASSUMABLE,
                    source_text=source_text,
                    reason=f"{unsupported_scope} budget is not supported by the deterministic planner",
                )
            )
        elif scope == ConstraintScope.HOTEL_TOTAL and strength == ConstraintStrength.UNSPECIFIED:
            ambiguities.append(
                RequirementAmbiguity(
                    level=AmbiguityLevel.BLOCKING,
                    source_text=source_text,
                    reason="Hotel amount does not specify a hard limit or a nightly/total policy",
                )
            )
        if not created_constraint:
            # An intervening non-canonical amount breaks the correction link.
            previous_scope = None
        previous_amount_end = amount.end()
    return merge_budget_constraints(candidates), ambiguities


def is_bounded_scope_correction(bridge: str) -> bool:
    """Accept only an immediate correction bridge after a monetary amount."""
    return bool(
        re.fullmatch(
            r"\s*(?:(?:total|maximum|ceiling)\s*)*(?:[.;]\s*|\s+(?:and|but)\s+)"
            r"(?:(?:actually|sorry)(?:,\s*)?)?\s*"
            r"(?:i\s+meant|(?:make|change)\s+(?:that|it|the\s+(?:total\s+trip|trip\s+total|total|trip|hotel))|"
            r"(?:no,\s*)?use|instead)(?:\s+to)?\s*",
            bridge,
            re.I,
        )
    )


def monetary_scope(prefix: str, suffix: str, intro: str = "") -> ConstraintScope | None:
    prefix = f"{prefix} {intro}".strip()
    immediate_suffix = suffix[:30]
    if re.match(r"\s*(?:per\s+(?:person|traveler)|each)\b", immediate_suffix, re.I):
        return None
    if re.search(r"\b(?:hotel|hotels|lodging|accommodation)\b", prefix, re.I) or re.search(
        r"\b(?:hotel|hotels|lodging|accommodation)\b", immediate_suffix, re.I
    ):
        if re.search(r"\bper\s+night\b", f"{prefix} {immediate_suffix}", re.I):
            return None
        return ConstraintScope.HOTEL_TOTAL
    if re.search(
        r"\b(?:total(?:\s+budget)?|keep\s+(?:the\s+)?trip|(?:whole|entire|full)\s+(?:the\s+)?trip|"
        r"everything|don't\s+let\s+(?:the\s+)?(?:total|trip|whole\s+trip)\s+go\s+over|"
        r"do\s+not\s+let\s+(?:the\s+)?(?:total|(?:total\s+)?trip)\s+go\s+over|"
        r"cap\s+(?:the\s+)?(?:whole\s+)?trip\s+at|(?:the\s+)?trip\s+budget|"
        r"(?:whole|entire|full)\s+trip\s+cap|"
        r"(?:the\s+)?trip\s+(?:(?:must|has\s+to|needs\s+to)\s+stay\s+)?"
        r"(?:under|below|up\s+to|max(?:imum)?|at\s+most|no\s+more\s+than|cannot\s+exceed|can't\s+go\s+above)|"
        r"\btrip\b[^.!?;]{0,40}\b(?:cannot\s+exceed|can't\s+go\s+above)\b|"
        r"\b(?:absolute\s+)?ceiling\b[^.!?;]{0,40}\btrip\b|\boverall\b)\b",
        prefix,
        re.I,
    ) or re.match(
        r"\s*(?:total|overall|for (?:the )?(?:(?:whole|entire|full) )?trip)\b", immediate_suffix, re.I
    ):
        return ConstraintScope.TOTAL_TRIP
    return None


def ambiguous_hotel_budget_phrase(prefix: str, intro: str, suffix: str) -> bool:
    """A bare 'hotel budget is' statement is not safely a total hard cap."""
    text = f"{prefix} {intro} {suffix[:30]}"
    return bool(
        re.search(r"\b(?:my\s+)?(?:hotel|lodging|accommodation)\s+budget\s*(?:is|of|:)?\b", text, re.I)
        and not re.search(r"\b(?:total|per\s+night|under|below|at\s+most|no\s+more)\b", text, re.I)
    )


def unsupported_money_scope(prefix: str, suffix: str) -> str | None:
    text = f"{prefix} {suffix[:30]}"
    if re.search(r"\b(?:hotel|lodging|accommodation)\b", text, re.I) and re.search(
        r"\bper\s+night\b", text, re.I
    ):
        return "HOTEL_PER_NIGHT"
    if re.search(r"\b(?:food|meals?|restaurants?)\b", text, re.I):
        return "FOOD_TOTAL"
    if re.search(r"\b(?:transport(?:ation)?|transit|flight)\b", text, re.I):
        return "TRANSPORT_TOTAL"
    if re.search(r"\b(?:attractions?|activities?|museum\s+tickets?)\b", text, re.I):
        return "ATTRACTIONS_TOTAL"
    return None


def has_unsupported_money_scope(prefix: str, suffix: str) -> bool:
    return unsupported_money_scope(prefix, suffix) is not None


def merge_budget_constraints(candidates: list[BudgetConstraint]) -> list[BudgetConstraint]:
    """Later mentions replace earlier ones only within the same semantic scope."""
    merged: dict[ConstraintScope, BudgetConstraint] = {}
    for candidate in candidates:
        merged[candidate.scope] = candidate
    return list(merged.values())


def legacy_budget_projection_match(query: str, amounts: list[re.Match]) -> re.Match | None:
    """Expose only total or scope-free money through the old one-budget fields."""
    compatible = []
    for amount in amounts:
        prefix, suffix = budget_context(query, amount)
        scope = monetary_scope(prefix, suffix, amount["intro"] or "")
        if scope == ConstraintScope.TOTAL_TRIP or (
            scope is None and not has_unsupported_money_scope(prefix, suffix)
        ):
            compatible.append(amount)
    total = [
        amount
        for amount in compatible
        if monetary_scope(*budget_context(query, amount), amount["intro"] or "")
        == ConstraintScope.TOTAL_TRIP
    ]
    return total[-1] if total else compatible[-1] if compatible else None


def budget_strength(context: str) -> ConstraintStrength:
    markers = [
        *((match.start(), ConstraintStrength.HARD) for match in BUDGET_HARD.finditer(context)),
        *((match.start(), ConstraintStrength.SOFT) for match in BUDGET_SOFT.finditer(context)),
    ]
    return max(markers, default=(-1, ConstraintStrength.UNSPECIFIED), key=lambda item: item[0])[1]


def budget_currency(amount: re.Match) -> str:
    value = (amount["code"] or amount["currency"] or amount["symbol"] or "USD").casefold()
    return {
        "$": "USD",
        "dollar": "USD",
        "dollars": "USD",
        "€": "EUR",
        "euro": "EUR",
        "euros": "EUR",
        "£": "GBP",
        "pound": "GBP",
        "pounds": "GBP",
    }.get(value, value.upper())


def extract_specific_preferences(query: str) -> list[SpecificPreference]:
    preferences = []
    for match in PREFERENCE_PATTERN.finditer(query):
        for raw in PREFERENCE_CONNECTOR.split(match["values"]):
            if BUDGET_PATTERN.search(raw):
                continue
            value = PREFERENCE_PREFIX.sub("", raw.strip()).strip().casefold()
            if not value or value in GENERIC_PREFERENCE_TERMS:
                continue
            value = {"zoos": "zoo"}.get(value, value)
            category = preference_category(value)
            if category == PreferenceCategory.FOOD and value.endswith(" food"):
                value = value.removesuffix(" food").strip()
            preference = SpecificPreference(category=category, value=value)
            if preference not in preferences:
                preferences.append(preference)
    for match in re.finditer(r"\b(?:want\s+to\s+)?visit\s+(?P<value>zoos?|museums?|parks?)\b", query, re.I):
        preference = SpecificPreference(
            category=PreferenceCategory.ACTIVITY,
            value={"zoos": "zoo"}.get(match["value"].casefold(), match["value"].casefold()),
        )
        if preference not in preferences:
            preferences.append(preference)
    return preferences


def extract_budget_preferences(query: str, amounts: list[re.Match]) -> list[SpecificPreference]:
    preferences = []
    for amount in amounts:
        prefix, suffix = budget_context(query, amount)
        scope = monetary_scope(prefix, suffix, amount["intro"] or "")
        category = (
            PreferenceCategory.HOTEL
            if scope == ConstraintScope.HOTEL_TOTAL
            or re.search(r"\b(?:hotel|hotels|lodging|accommodation)\b", f"{prefix} {suffix[:30]}", re.I)
            else PreferenceCategory.FOOD
            if re.search(r"\b(?:food|meal|restaurant)\b", f"{prefix} {suffix[:30]}", re.I)
            else None
        )
        if category is None:
            continue
        if budget_strength(f"{prefix} {amount['intro'] or ''} {suffix}") != ConstraintStrength.SOFT:
            continue
        rate = " per night" if re.search(r"\bper\s+night\b", suffix, re.I) else ""
        preferences.append(
            SpecificPreference(
                category=category,
                value=f"around {budget_currency(amount)} {amount['amount']}{rate}".casefold(),
            )
        )
    return [preference for index, preference in enumerate(preferences) if preference not in preferences[:index]]


def preference_category(value: str) -> PreferenceCategory:
    if re.fullmatch(r"(?:walking|public transit|taxi)", value):
        return PreferenceCategory.TRANSPORT
    if re.search(r"\b(?:city|urban|neighborhood)\s+walking\b", value):
        return PreferenceCategory.ACTIVITY
    if re.search(r"\b(?:zoos?|museums?|parks?)\b", value):
        return PreferenceCategory.ACTIVITY
    if re.search(r"\b(?:food|cuisine|meal|dish|coffee)\b", value) or re.match(
        r"(?:fried|grilled|baked|roasted|steamed)\b", value
    ):
        return PreferenceCategory.FOOD
    if re.search(r"\b(?:hotel|lodging|accommodation)\b", value):
        return PreferenceCategory.HOTEL
    return PreferenceCategory.UNSPECIFIED


def number_value(token: str) -> int:
    return NUMBER_WORDS[token.lower()] if token.lower() in NUMBER_WORDS else int(token)
