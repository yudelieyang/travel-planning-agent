// Mirrors app.openapi() after Phase A. Defaults are optional in OpenAPI;
// null and absent are kept distinct. No backend business rules live here.
export type PlanStatus = 'success' | 'needs_clarification' | 'error'
export type BudgetScope = 'TOTAL_TRIP' | 'PER_PERSON' | 'UNKNOWN'
export type ConstraintScope = 'TOTAL_TRIP' | 'HOTEL_TOTAL'
export type RequirementStatus = 'SUFFICIENT' | 'INSUFFICIENT'
export type Category = 'attractions' | 'hotel' | 'food' | 'transport'
export type SearchToolName = 'search_attractions' | 'search_hotels' | 'search_restaurants' | 'search_transport'
export type StageName = 'preflight' | 'clarification' | 'planner' | 'tools' | 'validation' | 'replan' | 'finalization'
export type StageOutcome = 'completed' | 'failed' | 'skipped' | 'not_reached' | 'clarification'
export type PlannerOutcome = 'not_invoked' | 'accepted' | 'failed'

export interface PlanRequest { query: string }

export interface TravelRequirements {
  destination?: string | null
  origin?: string | null
  start_date?: string | null
  end_date?: string | null
  duration_days?: number | null
  travelers?: number | null
  budget_amount?: number | null
  budget_scope?: BudgetScope
  budget_constraint_strength?: 'UNSPECIFIED' | 'HARD' | 'SOFT'
  objective?: OptimizationObjective | null
  currency?: string
  interests?: string[]
  hotel_preferences?: string[]
  food_preferences?: string[]
  transport_preferences?: string[]
  specific_preferences?: SpecificPreference[]
  constraints?: string[]
  requirements_v2?: RequirementsV2
}

export interface BudgetConstraint {
  kind: 'BUDGET'
  scope: ConstraintScope
  operator: 'LTE'
  value: number
  currency: string
  strength: 'HARD'
  source_text?: string | null
  extractor_source?: 'deterministic' | 'llm' | 'merged' | 'legacy_projection'
  confidence?: number
}

export type OptimizationObjective = 'maximize_budget_utilization'
export type PreferenceCategory = 'ACTIVITY' | 'FOOD' | 'HOTEL' | 'TRANSPORT' | 'UNSPECIFIED'
export interface SpecificPreference { category: PreferenceCategory; value: string }
export interface RequirementAmbiguity {
  level: 'RESOLVED' | 'ASSUMABLE' | 'BLOCKING'
  source_text: string
  reason: string
}
export interface RequirementsV2 {
  constraints?: BudgetConstraint[]
  preferences?: SpecificPreference[]
  objectives?: OptimizationObjective[]
  ambiguities?: RequirementAmbiguity[]
}

export interface SearchInput {
  destination: string
  max_price?: number | null
  preferences?: string[]
}

export interface TravelOption {
  id: string
  destination: string
  city?: string | null
  state?: string | null
  category?: Category | null
  name: string
  price: number
  currency?: 'USD'
  unit: 'per_person_visit' | 'per_person_night' | 'per_person_meal' | 'per_person_day'
  tags: string[]
  rating?: number | null
  review_count?: number | null
  image_url?: string | null
  source?: 'controlled_mock_fixture' | 'real_snapshot' | null
  description?: string | null
  preference_matches?: string[]
  address?: string | null
  latitude?: number | null
  longitude?: number | null
  provider?: string | null
  provider_place_id?: string | null
  provider_category_ids?: string[] | null
  provider_category_labels?: string[] | null
  provider_refreshed_at?: string | null
  snapshot_version?: string | null
  snapshot_fetched_at?: string | null
  cost_origin?: 'planner_estimate' | null
  cost_method?: string | null
  cost_version?: string | null
}

export interface CandidateGroup {
  category: Category
  selected: TravelOption[]
  alternatives: TravelOption[]
}

export interface CostItem { category: Category; amount: number }

export interface BudgetInput {
  items: CostItem[]
  travelers?: number | null
  limit?: number | null
  limit_currency?: string
  budget_scope?: BudgetScope
}

export interface BudgetSummary {
  currency?: 'USD'
  basis: 'group' | 'per_traveler'
  travelers: number | null
  per_traveler_cost: number
  estimated_total_cost: number
  breakdown: Partial<Record<Category, number>>
  provided_limit: number | null
  limit_currency: string
  budget_scope?: BudgetScope
  within_budget: boolean | null
  comparison_cost?: number | null
  remaining_budget?: number | null
  warnings: string[]
}

export interface Activity { name: string; category: Category; estimated_cost: number }
export interface DayPlan { day_number: number; activities: Activity[]; estimated_cost: number }
export interface Itinerary {
  destination: string
  days: number
  currency?: string
  estimated_total_cost: number
  daily_plan: DayPlan[]
  warnings?: string[]
}

export interface ExecutionStage {
  name: StageName
  sequence?: number | null
  outcome: StageOutcome
}

export interface ValidationSummary {
  performed?: boolean
  outcome?: 'passed' | 'failed' | 'not_performed'
  reason?: 'not_reached' | 'prior_errors' | 'missing_artifacts' | null
  violations?: ValidationViolation[]
}

export interface ValidationViolation {
  code: 'HARD_BUDGET_EXCEEDED' | 'HOTEL_BUDGET_EXCEEDED'
  category: 'budget'
  expected: number
  actual: number
  excess: number
  message: string
}

export interface SemanticExecutionSummary {
  mode: 'deterministic' | 'hybrid'
  coverage_triggered: boolean
  coverage_reasons: string[]
  llm_invoked: boolean
  extraction_status: 'not_requested' | 'proposed' | 'unavailable' | 'failed'
  final_source: 'deterministic' | 'hybrid'
  requires_clarification: boolean
  extractor_model?: string | null
  extractor_prompt_version?: string | null
}

export interface RepairChange { category: Category; before: string[]; after: string[] }
export interface RepairSummary {
  attempt: number
  maximum_attempts: 1
  trigger: ValidationViolation[]
  initial_total: number
  final_total?: number | null
  savings?: number | null
  final_outcome: 'passed' | 'failed'
  changes: RepairChange[]
}

export interface PublicToolRecord {
  tool_name: SearchToolName | 'calculate_budget'
  selected?: boolean
  executed: boolean
  execution_order?: number | null
  requested_arguments: SearchInput | BudgetInput | null
  runtime_arguments: SearchInput | BudgetInput | null
  status: 'SUCCESS' | 'NO_RESULTS' | 'ERROR' | 'SKIPPED'
  data?: TravelOption[] | BudgetSummary | null
  source?: 'mock' | 'snapshot' | 'deterministic' | null
  error_code?: 'tool_execution_failed' | 'UNSUPPORTED_CITY_DATA' | null
}

export interface PublicExecutionSummary {
  run_id: string
  mode: 'demo' | 'live' | 'custom'
  planner_type: string
  planner_invoked: boolean
  prompt_version: string | null
  latency_ms: number
  requirement_status: RequirementStatus
  planner_outcome: PlannerOutcome
  stages: ExecutionStage[]
  tools: PublicToolRecord[]
  validation: ValidationSummary
  replan_attempts?: number
  semantic?: SemanticExecutionSummary
  repair?: RepairSummary | null
  candidate_groups?: CandidateGroup[]
}

export interface PlanResponse {
  status: PlanStatus
  requirements: TravelRequirements
  itinerary?: Itinerary | null
  budget?: BudgetSummary | null
  missing_fields?: string[]
  clarification_question?: string | null
  warnings?: string[]
  errors?: string[]
  execution?: PublicExecutionSummary | null
}
