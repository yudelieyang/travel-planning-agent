import test, { before, after } from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { createServer } from 'vite'
import { createSSRApp } from 'vue'
import { renderToString } from 'vue/server-renderer'
import { budgetLabel, formatMoney, requirementState, sameSearchInputs } from '../src/utils/presentation.ts'

// Captured from the local deterministic backend for the five demo presets.
const plans = JSON.parse((await readFile(new URL('./fixtures/plans.json', import.meta.url), 'utf8')).replace(/^\uFEFF/, ''))
let server
before(async () => { server = await createServer({ server: { middlewareMode: true, hmr: false }, appType: 'custom' }) })
after(async () => { await server?.close() })
async function render(name, props) {
  const { default: component } = await server.ssrLoadModule(`/src/components/${name}.vue`)
  return renderToString(createSSRApp(component, props))
}
const text = html => html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ')

for (const scenario of ['nyc', 'boston', 'tight']) {
  test(`${scenario}: real completed history, accepted planner and successful tools`, async () => {
    const html = await render('ResultsShell', { response: plans[scenario] })
    assert.equal((html.match(/class="stage completed"/g) ?? []).length, 5)
    assert.equal((html.match(/class="stage /g) ?? []).length, 5)
    assert.equal((html.match(/tool-card tool-success/g) ?? []).length, 5)
    assert.match(html, /ACCEPTED/)
    assert.match(html, /PASSED/)
    assert.match(html, /Resolved runtime inputs/)
    assert.match(html, scenario === 'tight' ? /OVER BUDGET/ : /WITHIN BUDGET/)
    assert.doesNotMatch(html, /class="stage failed"/)
  })
}
test('clarification retains unreached stages and no tool cards', async () => {
  const html = await render('ResultsShell', { response: plans.clarification })
  assert.equal((html.match(/class="stage not_reached"/g) ?? []).length, 2)
  assert.equal((html.match(/MISSING — required/g) ?? []).length, 2)
  assert.match(html, /NOT INVOKED/)
  assert.match(html, /execution stopped at clarification/)
  assert.match(html, /No tools selected or executed/)
  assert.doesNotMatch(html, /tool-card/)
  assert.match(html, /NOT PERFORMED/)
})
test('Atlantis preserves failed tools, skipped budget and completed finalization', async () => {
  const html = await render('ResultsShell', { response: plans.atlantis })
  assert.equal((html.match(/tool-card tool-no_results/g) ?? []).length, 4)
  assert.match(html, /class="stage failed"/)
  assert.match(text(html), /Stage 5 Repair \/ final result FAILED/)
  assert.match(html, /Prior execution errors/)
  const budget = await render('ToolCallCard', { tool: plans.atlantis.execution.tools.find(t => t.tool_name === 'calculate_budget') })
  assert.match(text(budget), /Selected: Yes · Executed: No/)
  assert.match(budget, /SKIPPED/)
  assert.doesNotMatch(budget, /Resolved runtime inputs|Budget result|tool-error/)
  assert.match(html, /No itinerary produced/)
})
test('no response or absent execution never synthesizes history', async () => {
  for (const response of [null, { status: 'error', requirements: {}, execution: null }]) {
    const html = await render('ResultsShell', { response })
    assert.doesNotMatch(html, /class="stage |tool-card|Engineering diagnostics/)
  }
})
test('requirements distinguish null, empty arrays, missing fields, zero and constraints', async () => {
  const html = await render('RequirementsPanel', { requirements: { destination: null, origin: null, budget_amount: 0, currency: 'USD', interests: [], constraints: ['wheelchair access'] }, missingFields: ['destination', 'duration'] })
  assert.equal((html.match(/MISSING — required/g) ?? []).length, 2)
  assert.match(html, /Not supplied/)
  assert.match(html, /None extracted/)
  assert.match(html, /USD 0.00/)
  assert.match(html, /wheelchair access/)
  assert.match(html, /Legacy notes/)
  assert.equal(requirementState('duration_days', null, ['duration']), 'missing')
  assert.equal(requirementState('interests', [], []), 'empty')
  assert.equal(requirementState('budget_amount', 0, []), 'present')
})
test('search inputs are deduplicated only when equivalent and include result quote units', async () => {
  const tool = structuredClone(plans.boston.execution.tools[0])
  const html = await render('ToolCallCard', { tool })
  assert.match(html, /Approved requested \/ runtime inputs/)
  assert.match(html, /per person \/ visit/)
  tool.runtime_arguments.preferences = ['changed preference']
  const different = await render('ToolCallCard', { tool })
  assert.match(different, /Approved requested inputs/)
  assert.match(different, /Runtime inputs/)
  assert.doesNotMatch(different, /Approved requested \/ runtime inputs/)
  assert.equal(sameSearchInputs({ destination: 'Boston' }, { preferences: [], max_price: null, destination: 'Boston' }), true)
})
test('requirements show canonical hard constraints separately from legacy notes', async () => {
  const html = await render('RequirementsPanel', {
    requirements: {
      requirements_v2: { constraints: [
        { kind: 'BUDGET', scope: 'TOTAL_TRIP', operator: 'LTE', value: 900, currency: 'USD', strength: 'HARD' },
        { kind: 'BUDGET', scope: 'HOTEL_TOTAL', operator: 'LTE', value: 400, currency: 'USD', strength: 'HARD' },
      ] },
    },
    missingFields: [],
  })
  assert.match(html, /Hard constraints/)
  assert.match(html, /TOTAL TRIP ≤ USD 900\.00/)
  assert.match(html, /HOTEL TOTAL ≤ USD 400\.00/)
})
test('requirements expose semantic mode, preferences and ambiguity quarantine', async () => {
  const html = await render('RequirementsPanel', {
    requirements: {
      destination: 'Boston', duration_days: 3,
      requirements_v2: {
        constraints: [],
        preferences: [{ category: 'HOTEL', value: 'downtown' }],
        objectives: ['maximize_budget_utilization'],
        ambiguities: [{ level: 'BLOCKING', source_text: '$240 hotel', reason: 'Hotel amount has ambiguous scope.' }],
      },
    },
    missingFields: [],
    execution: { semantic: { mode: 'hybrid', coverage_triggered: true, coverage_reasons: ['AMBIGUOUS_SCOPE'], llm_invoked: true, extraction_status: 'proposed', final_source: 'hybrid', requires_clarification: true, extractor_model: 'test-model', extractor_prompt_version: 'semantic_extractor_v3' } },
  })
  for (const value of ['HYBRID', 'Coverage gate:', 'AMBIGUOUS SCOPE', 'downtown', 'MAXIMIZE BUDGET UTILIZATION', 'BLOCKING', 'clarification required', 'semantic_extractor_v3']) assert.ok(text(html).includes(value), value)
})
test('tool price semantics distinguish an unset search ceiling from the trip budget', async () => {
  const tool = structuredClone(plans.boston.execution.tools[0])
  const html = await render('ToolCallCard', { tool })
  assert.match(text(html), /Search price ceiling Not set/)
  assert.match(html, /Overall trip budget is enforced during itinerary budgeting and validation/)
  assert.match(html, /Candidate prices are still compared during planning/)
  assert.doesNotMatch(text(html), /Max price Not supplied/)
  assert.ok(html.includes(formatMoney(tool.data[0].price, tool.data[0].currency)))

  tool.requested_arguments.max_price = 50
  tool.runtime_arguments.max_price = 50
  assert.match(text(await render('ToolCallCard', { tool })), /Search price ceiling 50\.00/)
})
test('tool section shows a known overall budget without inventing one', async () => {
  const known = await render('ToolCallsPanel', { tools: plans.boston.execution.tools, requirements: plans.boston.requirements })
  assert.match(text(known), /Overall trip budget: USD 500\.00 total/)
  const absent = await render('ToolCallsPanel', { tools: plans.boston.execution.tools, requirements: { ...plans.boston.requirements, budget_amount: null } })
  assert.doesNotMatch(absent, /Overall trip budget:/)
})
test('tool ERROR remains distinct and public error code is readable', async () => {
  const html = await render('ToolCallCard', { tool: { ...plans.boston.execution.tools[0], status: 'ERROR', data: null, error_code: 'tool_execution_failed' } })
  assert.match(html, /tool-card tool-error/)
  assert.match(html, /TOOL EXECUTION FAILED/)
})
test('Candidate Explorer distinguishes selected options and preserved alternatives', async () => {
  const base = {
    destination: 'Columbus', city: 'Columbus', state: 'OH', category: 'food',
    price: 14, currency: 'USD', unit: 'per_person_meal', tags: ['fried chicken'],
    source: 'controlled_mock_fixture', preference_matches: ['fried chicken'], image_url: null,
  }
  const groups = [{
    category: 'food',
    selected: [{ ...base, id: 'cmh-f1', name: 'Mock Buckeye Fried Chicken', rating: 4.7, review_count: 860 }],
    alternatives: [{ ...base, id: 'cmh-f2', name: 'Mock North Market Chicken', rating: null, review_count: null }],
  }]
  const html = await render('CandidateExplorer', { groups })
  assert.match(html, /Candidate retrieval and selection/)
  assert.match(html, /Selected/)
  assert.match(html, /Alternative/)
  assert.match(html, /4\.7 · 860 demo reviews/)
  assert.doesNotMatch(html, /Rating not supplied|0\.0 rating|0 reviews/)
  assert.match(html, /Selected with explicit preference match: fried chicken/)
  assert.match(html, /Controlled mock fixture/)
  assert.doesNotMatch(html, /<img/)
  assert.match(text(html), /1 selected · 1 alternatives/)
  assert.match(text(html), /source total before filtering is not exposed/i)
})

test('Candidate Explorer labels real POIs and synthetic transport at section level', async () => {
  const snapshot = { category: 'attractions', selected: [{ id: 'bos-a1', destination: 'Boston', category: 'attractions', name: 'Boston Public Garden', price: 12, currency: 'USD', unit: 'per_person_visit', tags: ['parks'], source: 'real_snapshot', provider: 'openstreetmap' }], alternatives: [] }
  const transport = { category: 'transport', selected: [{ id: 'bos-t1', destination: 'Boston', category: 'transport', name: 'Walking', price: 0, currency: 'USD', unit: 'per_person_day', tags: ['walking'], source: 'controlled_mock_fixture' }], alternatives: [] }
  const visible = text(await render('CandidateExplorer', { groups: [snapshot, transport] }))
  assert.match(visible, /Real-world OpenStreetMap snapshot · frozen, not live/)
  assert.match(visible, /Synthetic planning allowance/)
})

test('Candidate Explorer separates OSM place facts from planner estimates', async () => {
  const option = {
    id: 'bos-a1', destination: 'Boston', city: 'Boston', state: 'MA', category: 'attractions',
    name: 'Isabella Stewart Gardner Museum', address: '25 Evans Way, Boston, MA 02115',
    latitude: 42.3382381, longitude: -71.0990448, price: 20, currency: 'USD',
    unit: 'per_person_visit', tags: ['museums'], source: 'real_snapshot',
    provider: 'openstreetmap', provider_place_id: 'way/29650851',
    provider_category_ids: ['tourism=museum'], provider_category_labels: ['Museum'],
    snapshot_version: 'osm_boston_attractions_2026-09-16_v1',
    snapshot_fetched_at: '2026-09-16T05:36:07.2890118Z',
    cost_origin: 'planner_estimate', cost_method: 'legacy_demo_cost_preserved_for_phase_o_migration',
    cost_version: 'phase_o_v1', rating: null, review_count: null, preference_matches: [],
  }
  const html = await render('CandidateExplorer', { groups: [{ category: 'attractions', selected: [option], alternatives: [] }] })
  const visible = text(html)
  for (const value of ['Isabella Stewart Gardner Museum', '25 Evans Way, Boston, MA 02115', 'Planner estimate:', 'USD 20.00', 'per traveler / visit', 'OpenStreetMap snapshot', '© OpenStreetMap contributors', 'ODbL']) assert.ok(visible.includes(value), value)
  assert.doesNotMatch(visible, /Rating not supplied|0\.0 rating|0 reviews|way\/29650851/)
})

test('Candidate Explorer labels OSM hotel costs per traveler and omits fake reputation data', async () => {
  const option = {
    id: 'bos-h1', destination: 'Boston', city: 'Boston', state: 'MA', category: 'hotel',
    name: 'Boston Harbor Hotel', address: '70 Rowes Wharf, Boston, MA 02110',
    latitude: 42.3566602, longitude: -71.0503163, price: 100, currency: 'USD',
    unit: 'per_person_night', tags: ['central', 'budget'], source: 'real_snapshot',
    provider: 'openstreetmap', provider_place_id: 'node/1325873780',
    provider_category_ids: ['tourism=hotel'], provider_category_labels: ['Hotel'],
    snapshot_version: 'osm_boston_hotels_2026-09-16_v1',
    snapshot_fetched_at: '2026-09-16T06:26:35.9245460Z',
    cost_origin: 'planner_estimate', cost_method: 'legacy_demo_cost_preserved_for_phase_o_migration',
    cost_version: 'phase_o_v1', rating: null, review_count: null, preference_matches: [],
  }
  const html = await render('CandidateExplorer', { groups: [{ category: 'hotel', selected: [option], alternatives: [] }] })
  const visible = text(html)
  for (const value of ['Boston Harbor Hotel', '70 Rowes Wharf, Boston, MA 02110', 'Planner estimate:', 'USD 100.00', 'per traveler / night', 'OpenStreetMap snapshot', '© OpenStreetMap contributors']) assert.ok(visible.includes(value), value)
  assert.doesNotMatch(visible, /Rating not supplied|0\.0 rating|0 reviews|node\/1325873780|actual room rate/i)
})
test('Candidate Explorer separates OSM cuisine from planner food tags and estimates', async () => {
  const option = {
    id: 'bos-f1', destination: 'Boston', city: 'Boston', state: 'MA', category: 'food',
    name: 'Aceituna Grill', address: '267 Newbury Street, Boston, MA 02116',
    latitude: 42.3495341, longitude: -71.0834556, price: 16, currency: 'USD',
    unit: 'per_person_meal', tags: ['vegetarian', 'vegan'], source: 'real_snapshot',
    provider: 'openstreetmap', provider_place_id: 'node/12663666560',
    provider_category_ids: ['amenity=restaurant', 'cuisine=mediterranean', 'diet:vegetarian=yes', 'diet:vegan=yes'],
    provider_category_labels: ['Restaurant', 'Cuisine: Mediterranean', 'Vegetarian options', 'Vegan options'],
    snapshot_version: 'osm_boston_food_2026-09-16_v1',
    snapshot_fetched_at: '2026-09-16T12:07:21.440541Z',
    cost_origin: 'planner_estimate', cost_method: 'legacy_demo_cost_preserved_for_phase_o_migration',
    cost_version: 'phase_o_v1', rating: null, review_count: null, preference_matches: ['vegetarian'],
  }
  const html = await render('CandidateExplorer', { groups: [{ category: 'food', selected: [option], alternatives: [] }] })
  const visible = text(html)
  for (const value of ['Aceituna Grill', '267 Newbury Street, Boston, MA 02116', 'Cuisine: mediterranean', 'Planner estimate:', 'USD 16.00', 'per traveler / meal', 'Planner preference tags:', 'vegetarian', 'vegan', 'OpenStreetMap snapshot', '© OpenStreetMap contributors']) assert.ok(visible.includes(value), value)
  assert.doesNotMatch(visible, /Rating not supplied|0\.0 rating|0 reviews|node\/12663666560|actual meal price/i)
})

test('top-level status and result disclosure distinguish snapshot, estimates and mock data', async () => {
  const snapshot = structuredClone(plans.boston)
  for (const tool of snapshot.execution.tools.slice(0, 3)) tool.source = 'snapshot'
  const header = text(await render('DemoHeader', { execution: snapshot.execution }))
  for (const value of ['REAL-WORLD SNAPSHOT POIs', 'Frozen OpenStreetMap POIs', 'Planner-estimated costs', 'Synthetic transport']) assert.ok(header.includes(value), value)
  assert.doesNotMatch(header, /LIVE DATA/)
  assert.match(text(await render('DemoHeader', { execution: plans.boston.execution })), /CONTROLLED MOCK CANDIDATES/)
  assert.match(text(await render('DemoHeader', { execution: plans.clarification.execution })), /CANDIDATE DATA NOT USED/)
  assert.match(text(await render('DemoHeader', { execution: null })), /candidate data mode will be confirmed/i)
  assert.match(text(await render('ResultsShell', { response: snapshot })), /POIs come from frozen OpenStreetMap snapshots; costs are planner estimates, and transport is a synthetic allowance/)
  assert.match(text(await render('ResultsShell', { response: plans.boston })), /Controlled candidate data and costs are deterministic demo estimates/)
})
test('validation covers every public reason and failed outcome', async () => {
  for (const [reason, label] of [['prior_errors', 'Prior execution errors'], ['not_reached', 'Validation was not reached'], ['missing_artifacts', 'Required artifacts were missing']]) {
    const html = await render('ValidationPanel', { validation: { performed: false, outcome: 'not_performed', reason } })
    assert.match(html, /NOT PERFORMED/)
    assert.ok(html.includes(label))
  }
  assert.match(await render('ValidationPanel', { validation: { performed: true, outcome: 'failed' } }), /FAILED/)
})
test('validation renders typed violation and bounded repair evidence', async () => {
  const repair = {
    attempt: 1, maximum_attempts: 1,
    trigger: [{ code: 'HARD_BUDGET_EXCEEDED', category: 'budget', expected: 350, actual: 394, excess: 44, message: 'Hard budget exceeded' }],
    initial_total: 394, final_total: 317, savings: 77, final_outcome: 'passed',
    changes: [{ category: 'food', before: ['Higher-cost choice'], after: ['Lower-cost choice'] }],
  }
  const html = text(await render('ValidationPanel', { validation: { performed: true, outcome: 'passed' }, repair }))
  for (const value of ['Repair attempt 1 of 1', 'HARD BUDGET EXCEEDED', 'USD 394.00', 'USD 317.00', 'USD 77.00 saved', 'Higher-cost choice → Lower-cost choice', 'no infinite loop']) assert.ok(html.includes(value), value)
})
test('repaired final validation is successful in the five-stage summary', async () => {
  const execution = { ...plans.boston.execution, repair: { final_outcome: 'passed' }, validation: { performed: true, outcome: 'passed' }, stages: [...plans.boston.execution.stages, { name: 'validation', sequence: 6, outcome: 'failed' }] }
  const html = text(await render('ExecutionPipeline', { execution, status: 'success' }))
  assert.match(html, /Stage 4 Validation COMPLETED Initial validation failed; repair revalidated successfully/)
})
test('pipeline condenses backend history into the five recruiter stages', async () => {
  const stages = [{ name: 'preflight', sequence: 1, outcome: 'clarification' }, { name: 'clarification', sequence: 2, outcome: 'completed' }, { name: 'tools', sequence: 3, outcome: 'failed' }, { name: 'validation', sequence: 4, outcome: 'skipped' }, { name: 'planner', sequence: null, outcome: 'not_reached' }]
  const execution = { ...plans.boston.execution, stages, requirement_status: 'INSUFFICIENT', validation: { performed: false, outcome: 'not_performed' } }
  const html = await render('ExecutionPipeline', { execution, status: 'needs_clarification' })
  assert.equal((html.match(/class="stage /g) ?? []).length, 5)
  for (const label of ['User request', 'Requirements understanding', 'Candidate retrieval / selection', 'Validation', 'Repair / final result']) assert.ok(html.includes(label))
  for (const outcome of ['CLARIFICATION', 'COMPLETED', 'FAILED', 'SKIPPED']) assert.ok(html.includes(outcome))
})
test('diagnostics start collapsed and render only approved public fields', async () => {
  const html = await render('DiagnosticsDrawer', { execution: { ...plans.boston.execution, secret: 'NEVER_RENDER', messages: ['NEVER_RENDER'] } })
  assert.match(html, /<details class="panel diagnostics">/)
  assert.doesNotMatch(html, / open|NEVER_RENDER/)
  assert.match(html, /Run ID/)
})
test('unknown budget comparisons and null money are not zero', () => {
  assert.equal(budgetLabel(null), 'Comparison unavailable')
  assert.equal(formatMoney(null), 'Not supplied')
  assert.equal(formatMoney(0, 'USD'), 'USD 0.00')
})

test('Phase D Boston budget has exact totals, balance and category breakdown', async () => {
  const html = await render('BudgetSummary', { budget: plans.boston.budget })
  for (const value of ['USD 223.00', 'USD 500.00', 'USD 277.00 remaining', 'WITHIN BUDGET', 'Group total', 'Cost breakdown', 'Hotel', 'Food', 'Transport', 'Attraction']) assert.ok(html.includes(value), value)
})
test('Phase D tight budget keeps full successful itinerary and explains overage', async () => {
  assert.equal(plans.tight.status, 'success')
  const html = await render('ResultsShell', { response: plans.tight })
  for (const value of ['USD 446.00', 'USD 50.00', 'USD 396.00 over budget', 'OVER BUDGET', 'Day 1', 'Day 2', 'PASSED']) assert.ok(html.includes(value), value)
  assert.doesNotMatch(html, /Planning failed/)
})
test('Phase D unknown comparison never manufactures a remaining amount', async () => {
  const budget = { ...plans.boston.budget, within_budget: null, comparison_cost: null, remaining_budget: null, budget_scope: 'UNKNOWN' }
  const html = await render('BudgetSummary', { budget })
  assert.match(html, /COMPARISON UNAVAILABLE/)
  assert.match(html, /Budget scope unknown/)
  assert.doesNotMatch(html, /USD 0.00 remaining|USD 277.00 remaining/)
})
test('Phase D no budget limit preserves estimate without a comparison', async () => {
  const budget = { ...plans.boston.budget, provided_limit: null, within_budget: null, comparison_cost: null, remaining_budget: null }
  const html = await render('BudgetSummary', { budget })
  assert.match(html, /NO BUDGET PROVIDED/)
  assert.match(html, /No budget limit provided/)
  assert.match(html, /USD 223.00/)
  assert.doesNotMatch(html, /USD 0.00 remaining/)
})
test('Phase D per-person budget and group estimate remain separate', async () => {
  const budget = { ...plans.tight.budget, budget_scope: 'PER_PERSON', provided_limit: 500, comparison_cost: 223, remaining_budget: 277, within_budget: true }
  const html = text(await render('BudgetSummary', { budget }))
  assert.match(html, /Estimated group trip cost USD 446.00/)
  assert.match(html, /Budget per traveler USD 500.00/)
  assert.match(html, /Compared cost per traveler USD 223.00/)
  assert.match(html, /Budget balance per traveler USD 277.00 remaining/)
})
test('Phase D unknown travelers use per-traveler estimate labels', async () => {
  const budget = { ...plans.boston.budget, basis: 'per_traveler', travelers: null, within_budget: null, comparison_cost: null, remaining_budget: null }
  const html = text(await render('BudgetSummary', { budget }))
  assert.match(html, /Estimated trip cost per traveler USD 223.00/)
  assert.doesNotMatch(html, /Group total|1 traveler/)
})
test('Phase D empty results have contextual explanations and no fake days or zero amounts', async () => {
  for (const scenario of ['clarification', 'atlantis']) {
    const response = plans[scenario]
    const budget = await render('BudgetSummary', { budget: null, status: response.status, execution: response.execution })
    const itinerary = await render('ItinerarySummary', { itinerary: null, status: response.status, execution: response.execution })
    assert.match(budget, scenario === 'clarification' ? /was not reached/ : /was skipped/)
    assert.match(itinerary, scenario === 'clarification' ? /Complete the required trip details/ : /Search tools returned no usable travel options/)
    assert.match(itinerary, /No itinerary produced/)
    assert.doesNotMatch(budget + itinerary, /USD 0.00|Day 1|day-card/)
  }
})
test('Phase D itinerary preserves every name, day, category and backend total', async () => {
  for (const scenario of ['boston', 'nyc', 'tight']) {
    const { itinerary, budget } = plans[scenario]
    // Consistency check is a test only; the UI never replaces either total.
    assert.equal(itinerary.estimated_total_cost, budget.estimated_total_cost)
    const html = await render('ItinerarySummary', { itinerary, basis: budget.basis })
    assert.equal((html.match(/class="day-card"/g) ?? []).length, itinerary.daily_plan.length)
    assert.equal((html.match(/class="activity-category"/g) ?? []).length, itinerary.daily_plan.flatMap(day => day.activities).length)
    for (const day of itinerary.daily_plan) {
      assert.ok(html.includes(`Day ${day.day_number}`))
      assert.ok(html.includes(formatMoney(day.estimated_cost, itinerary.currency)))
      for (const activity of day.activities) assert.ok(html.includes(activity.name))
    }
    for (const category of ['Attraction', 'Food', 'Transport', 'Hotel']) assert.ok(html.includes(category))
    assert.ok(html.includes(formatMoney(itinerary.estimated_total_cost, itinerary.currency)))
  }
})
test('Phase D warnings from all three sources are retained once', async () => {
  const response = structuredClone(plans.boston)
  response.warnings = ['Shared warning']
  response.budget.warnings = ['Shared warning', 'Budget-only warning']
  response.itinerary.warnings = ['Shared warning', 'Itinerary-only warning']
  const html = await render('ResultsShell', { response })
  for (const warning of ['Shared warning', 'Budget-only warning', 'Itinerary-only warning']) assert.equal(html.split(warning).length - 1, 1)
})
test('Phase D remaining zero is valid and currency units stay separate', async () => {
  const budget = { ...plans.boston.budget, remaining_budget: 0, within_budget: true }
  assert.match(await render('BudgetSummary', { budget }), /USD 0.00 remaining/)
  const incompatible = { ...budget, limit_currency: 'EUR', within_budget: null, comparison_cost: null, remaining_budget: null }
  const html = await render('BudgetSummary', { budget: incompatible })
  assert.match(html, /EUR 500.00/)
  assert.match(html, /USD 223.00/)
  assert.match(html, /COMPARISON UNAVAILABLE/)
})


import { presets, findScenario } from '../src/presets.ts'
import { demoTakeaway } from '../src/utils/demo.ts'

test('Phase E exact scenario identity and selector semantics', async () => {
  assert.equal(presets.length, 6)
  for (const preset of presets) {
    assert.equal(findScenario(preset.query)?.id, preset.id)
    assert.equal(findScenario(preset.query + ' '), null)
    const html = await render('TravelRequestPanel', { modelValue: preset.query, submitting: false })
    assert.match(html, /aria-pressed="true"/)
    assert.ok(html.includes(preset.description))
    assert.ok(html.includes(preset.query.replaceAll('&', '&amp;')))
  }
  const custom = await render('TravelRequestPanel', { modelValue: 'Custom destination', submitting: false })
  assert.match(custom, /Custom Request/)
  assert.doesNotMatch(custom, /aria-pressed="true"/)
})
test('demo shortcuts use capability-first labels and preserve scenario requests', async () => {
  const html = await render('TravelRequestPanel', { modelValue: '', submitting: false })
  for (const value of ['Try a demo scenario', 'optional shortcuts', 'specific agent behaviors', 'Real Snapshot Trip', 'Preference Matching', 'Ambiguity Boundary', 'Correction Safety', 'Tradeoff Boundary', 'Bounded Budget Repair', 'Custom Request']) {
    if (value === 'Custom Request') continue
    assert.ok(text(html).includes(value), value)
  }
  assert.match(html, /aria-label="Demo scenario shortcuts"/)
  assert.match(presets.find(preset => preset.id === 'snapshot')?.query ?? '', /Boston/)
  assert.match(presets.find(preset => preset.id === 'deterministic')?.query ?? '', /Columbus/)
  assert.match(presets.find(preset => preset.id === 'ambiguity')?.query ?? '', /\$240 hotel/)
  assert.match(presets.find(preset => preset.id === 'correction')?.query ?? '', /revise lodging to \$525/)
  assert.match(presets.find(preset => preset.id === 'tradeoff')?.query ?? '', /if it is downtown/)
  assert.match(presets.find(preset => preset.id === 'repair')?.query ?? '', /budget is \$350/)
  assert.equal(presets.some(preset => preset.query.includes('Atlantis')), false)
})
test('travel request guidance gives concise fields, example and budget wording', async () => {
  const html = await render('TravelRequestPanel', { modelValue: '', submitting: false })
  for (const value of [
    'Tips for a better request',
    'destination, duration or dates, travelers, total budget',
    'use Real Snapshot Trip, then Bounded Budget Repair or Preference Matching',
    'total budget of $1300',
    'around $1300',
    'Optional details can be omitted',
    'Plan Trip',
    'Reset',
  ]) assert.ok(html.includes(value), value)
  assert.match(html, /aria-describedby="request-guidance query-help"/)
  assert.equal((html.match(/aria-pressed="false"/g) ?? []).length, presets.length)
})
test('Phase E takeaway uses actual success, clarification and budget evidence', () => {
  assert.match(demoTakeaway(plans.boston).join(' '), /Every recorded tool executed successfully/)
  assert.match(demoTakeaway(plans.boston).join(' '), /Validation was performed and passed/)
  assert.match(demoTakeaway(plans.clarification).join(' '), /planner was not invoked/)
  const tight = demoTakeaway(plans.tight).join(' ')
  assert.match(tight, /completed successfully/)
  assert.match(tight, /exceeds the supplied budget/)
  const failure = demoTakeaway(plans.atlantis).join(' ')
  assert.match(failure, /executed searches returned no usable/)
  assert.match(failure, /Budget calculation was skipped/)
  assert.match(failure, /Validation was not performed/)
})
test('Phase E unexpected response overrides scenario expectations and unsupported claims are absent', async () => {
  const html = await render('DemoTakeaway', { submittedQuery: presets[0].query, response: plans.atlantis })
  assert.match(html, /domain error/)
  assert.doesNotMatch(html, /completed successfully|within the supplied budget/)
  const noEvidence = demoTakeaway({ status: 'success', requirements: {}, execution: null }).join(' ')
  assert.doesNotMatch(noEvidence, /tools|Validation|budget|optimized/)
  const changed = structuredClone(plans.boston)
  changed.execution.tools[0].status = 'ERROR'
  changed.execution.validation.performed = false
  assert.doesNotMatch(demoTakeaway(changed).join(' '), /Every recorded tool|performed and passed/)
})
test('Phase E no stale takeaway for custom, pending or reset state', async () => {
  for (const props of [{ submittedQuery: 'custom', response: plans.boston }, { submittedQuery: presets[0].query, response: null }, { submittedQuery: '', response: null }]) {
    assert.doesNotMatch(await render('DemoTakeaway', props), /Demo takeaway/)
  }
})
