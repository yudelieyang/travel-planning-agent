import type { PlanResponse } from '../types/travel.ts'

// Independent observable facts; never consult scenario names or expected amounts.
export function demoTakeaway(response: PlanResponse | null): string[] {
  if (!response) return []
  const facts: string[] = []
  const execution = response.execution
  if (response.status === 'needs_clarification') {
    facts.push('The request requires clarification.')
    if (response.missing_fields?.length && execution?.planner_invoked === false && execution.stages.some(stage => stage.name === 'preflight' && stage.outcome === 'clarification')) {
      facts.push('Preflight identified missing required details; the planner was not invoked.')
    }
  } else if (response.status === 'success') {
    facts.push('The request completed successfully.')
  } else {
    facts.push('The request returned a domain error.')
  }
  if (execution) {
    if (execution.validation.performed === true && execution.validation.outcome === 'passed') facts.push('Validation was performed and passed.')
    if (execution.tools.length && execution.tools.every(tool => tool.executed && tool.status === 'SUCCESS')) facts.push('Every recorded tool executed successfully.')
    const searches = execution.tools.filter(tool => tool.tool_name !== 'calculate_budget' && tool.executed)
    if (searches.length && searches.every(tool => tool.status === 'NO_RESULTS')) facts.push('The executed searches returned no usable travel options.')
    if (execution.tools.some(tool => tool.tool_name === 'calculate_budget' && !tool.executed && tool.status === 'SKIPPED')) facts.push('Budget calculation was skipped.')
    if (execution.validation.performed === false) facts.push('Validation was not performed.')
  }
  if (response.budget?.within_budget === false) facts.push('The estimate exceeds the supplied budget.')
  else if (response.budget?.within_budget === true) facts.push('The estimate is within the supplied budget.')
  if (response.status === 'error' && !response.itinerary) facts.push('No itinerary was produced.')
  return facts
}
