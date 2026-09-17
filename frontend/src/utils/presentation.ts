import type { BudgetInput, SearchInput, TravelRequirements } from '../types/travel.ts'

export function formatMoney(value: number | null | undefined, currency?: string) {
  return value == null ? 'Not supplied' : `${currency ?? ''} ${value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`.trim()
}
export function formatEnumLabel(value: string | null | undefined) {
  return value == null ? 'Not reported' : value.replaceAll('_', ' ').toUpperCase()
}
export function budgetLabel(value: boolean | null | undefined) {
  return value === true ? 'WITHIN BUDGET' : value === false ? 'OVER BUDGET' : 'Comparison unavailable'
}
export function yesNo(value: boolean | undefined) {
  return value == null ? 'Not reported' : value ? 'Yes' : 'No'
}
export const toolNames = {
  search_attractions: 'Attraction Search', search_hotels: 'Hotel Search',
  search_restaurants: 'Restaurant Search', search_transport: 'Transport Search', calculate_budget: 'Budget Calculator',
}
export const stageNames = {
  preflight: 'Preflight', clarification: 'Clarification', planner: 'Planner',
  tools: 'Tools', validation: 'Validation', replan: 'Budget repair', finalization: 'Finalization',
}
export const validationReasons = {
  prior_errors: 'Prior execution errors', not_reached: 'Validation was not reached', missing_artifacts: 'Required artifacts were missing',
}
export const quoteUnits = {
  per_person_visit: 'per person / visit', per_person_night: 'per person / night',
  per_person_meal: 'per person / meal', per_person_day: 'per person / day',
}
export function requirementState(key: keyof TravelRequirements, value: unknown, missing: string[]) {
  if (missing.includes(key) || (key === 'duration_days' && missing.includes('duration'))) return 'missing'
  if (Array.isArray(value) && value.length === 0) return 'empty'
  return value == null || value === '' ? 'absent' : 'present'
}
export function isSearchInput(value: SearchInput | BudgetInput | null): value is SearchInput {
  return value != null && 'destination' in value
}
export function sameSearchInputs(left: SearchInput | BudgetInput | null, right: SearchInput | BudgetInput | null) {
  return isSearchInput(left) && isSearchInput(right) && left.destination === right.destination
    && (left.max_price ?? null) === (right.max_price ?? null)
    && JSON.stringify(left.preferences ?? []) === JSON.stringify(right.preferences ?? [])
}

export const categoryLabels = { attractions: 'Attraction', hotel: 'Hotel', food: 'Food', transport: 'Transport' }
export function formatCostBasis(basis: 'group' | 'per_traveler' | undefined) {
  return basis === 'group' ? 'Group total' : basis === 'per_traveler' ? 'Per traveler' : 'Cost basis not reported'
}
export function formatBudgetScope(scope: string | undefined) {
  return scope === 'TOTAL_TRIP' ? 'Whole trip budget' : scope === 'PER_PERSON' ? 'Budget per traveler' : 'Budget scope unknown'
}
export function resultBudgetStatus(budget: { within_budget: boolean | null; provided_limit: number | null }) {
  if (budget.within_budget === true) return 'WITHIN BUDGET'
  if (budget.within_budget === false) return 'OVER BUDGET'
  return budget.provided_limit == null ? 'NO BUDGET PROVIDED' : 'COMPARISON UNAVAILABLE'
}
export function formatRemainingBudget(value: number | null | undefined, currency: string) {
  if (value == null) return 'Comparison unavailable'
  return value < 0 ? `${formatMoney(Math.abs(value), currency)} over budget` : `${formatMoney(value, currency)} remaining`
}
export function uniqueWarnings(...groups: (string[] | undefined)[]) {
  return [...new Set(groups.flatMap(group => group ?? []))]
}
