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
    assert.equal((html.match(/class="stage not_reached"/g) ?? []).length, 1)
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
  assert.equal((html.match(/class="stage not_reached"/g) ?? []).length, 4)
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
  assert.match(text(html), /Step 5 Finalization COMPLETED/)
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
  assert.match(html, /None supplied/)
  assert.match(html, /USD 0.00/)
  assert.match(html, /wheelchair access/)
  assert.match(html, /not all are enforced/)
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
test('tool ERROR remains distinct and public error code is readable', async () => {
  const html = await render('ToolCallCard', { tool: { ...plans.boston.execution.tools[0], status: 'ERROR', data: null, error_code: 'tool_execution_failed' } })
  assert.match(html, /tool-card tool-error/)
  assert.match(html, /TOOL EXECUTION FAILED/)
})
test('validation covers every public reason and failed outcome', async () => {
  for (const [reason, label] of [['prior_errors', 'Prior execution errors'], ['not_reached', 'Validation was not reached'], ['missing_artifacts', 'Required artifacts were missing']]) {
    const html = await render('ValidationPanel', { validation: { performed: false, outcome: 'not_performed', reason } })
    assert.match(html, /NOT PERFORMED/)
    assert.ok(html.includes(label))
  }
  assert.match(await render('ValidationPanel', { validation: { performed: true, outcome: 'failed' } }), /FAILED/)
})
test('pipeline preserves backend order, sequence and all outcomes', async () => {
  const stages = [{ name: 'preflight', sequence: 1, outcome: 'clarification' }, { name: 'clarification', sequence: 2, outcome: 'completed' }, { name: 'tools', sequence: 3, outcome: 'failed' }, { name: 'validation', sequence: 4, outcome: 'skipped' }, { name: 'planner', sequence: null, outcome: 'not_reached' }]
  const html = await render('ExecutionPipeline', { stages })
  assert.ok(html.indexOf('Step 4') < html.indexOf('>Unreached</span>'))
  for (const outcome of ['CLARIFICATION', 'COMPLETED', 'FAILED', 'SKIPPED', 'NOT REACHED']) assert.ok(html.includes(outcome))
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
  assert.equal(presets.length, 5)
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
