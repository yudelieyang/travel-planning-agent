export const presets = [
  { id: 'boston', label: 'Boston', purpose: 'Happy-path planning', description: 'Demonstrates end-to-end planning, tool orchestration, and result validation.', query: 'Plan a 2-day trip to Boston for 1 traveler under $500 total.' },
  { id: 'nyc', label: 'NYC', purpose: 'Preference extraction', description: 'Demonstrates how structured preferences flow into travel planning.', query: 'Plan a 3-day trip to New York City for 1 traveler under $1000 total. I like museums and vegetarian food.' },
  { id: 'clarification', label: 'Clarification', purpose: 'Missing-input guardrail', description: 'Demonstrates how the system handles missing required trip details.', query: 'Plan a trip for me.' },
  { id: 'tight', label: 'Tight Budget', purpose: 'Constraint violation', description: 'Demonstrates the distinction between successful execution and satisfying a budget.', query: 'Plan a 2-day trip to Boston for 2 travelers under $50 total.' },
  { id: 'atlantis', label: 'Atlantis', purpose: 'Unavailable travel data', description: 'Demonstrates how the system handles unavailable travel data.', query: 'Plan a 2-day trip to Atlantis.' },
] as const

export function findScenario(query: string) {
  return presets.find(scenario => scenario.query === query) ?? null
}
