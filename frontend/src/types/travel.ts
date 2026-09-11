// Mirrors app.openapi() after Phase A. Defaults are optional in OpenAPI;
// null and absent are kept distinct. No backend business rules live here.
export type PlanStatus = 'success' | 'needs_clarification' | 'error'
export type BudgetScope = 'TOTAL_TRIP' | 'PER_PERSON' | 'UNKNOWN'
export type RequirementStatus = 'SUFFICIENT' | 'INSUFFICIENT'
export type Category = 'attractions' | 'hotel' | 'food' | 'transport'
export type SearchToolName = 'search_attractions' | 'search_hotels' | 'search_restaurants' | 'search_transport'
export type StageName = 'preflight' | 'clarification' | 'planner' | 'tools' | 'validation' | 'finalization'
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
  currency?: string
  interests?: string[]
  hotel_preferences?: string[]
  food_preferences?: string[]
  transport_preferences?: string[]
  constraints?: string[]
}

export interface SearchInput {
  destination: string
  max_price?: number | null
  preferences?: string[]
}

export interface TravelOption {
  id: string
  destination: string
  name: string
  price: number
  currency?: 'USD'
  unit: 'per_person_visit' | 'per_person_night' | 'per_person_meal' | 'per_person_day'
  tags: string[]
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
  source?: 'mock' | 'deterministic' | null
  error_code?: 'tool_execution_failed' | null
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
