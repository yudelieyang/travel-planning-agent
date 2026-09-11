import test from 'node:test'
import assert from 'node:assert/strict'
import { effectScope } from 'vue'
import { useTravelPlan } from '../src/composables/useTravelPlan.ts'
import { ApiError } from '../src/api/travelApi.ts'

const result = { status: 'success', requirements: {}, execution: null }
function setup(t, send) {
  const scope = effectScope()
  t.after(() => scope.stop())
  return scope.run(() => useTravelPlan(send))
}

test('empty input is blocked but missing travel details are submitted', async (t) => {
  const calls = []
  const state = setup(t, async request => { calls.push(request); return result })
  state.draftQuery.value = '   '
  await state.submit()
  assert.equal(calls.length, 0)
  state.draftQuery.value = 'Plan a trip for me.'
  await state.submit()
  assert.deepEqual(calls, [{ query: 'Plan a trip for me.' }])
  assert.equal(state.requestState.value, 'settled')
})

test('pending request blocks duplicates and does not fabricate stage progress', async (t) => {
  let resolve
  let calls = 0
  const state = setup(t, () => { calls++; return new Promise(done => { resolve = done }) })
  state.draftQuery.value = 'Boston'
  const pending = state.submit()
  await state.submit()
  assert.equal(calls, 1)
  assert.equal(state.requestState.value, 'submitting')
  assert.equal(state.response.value, null)
  resolve(result)
  await pending
  assert.equal(state.response.value, result)
})

test('editing clears previous response and old submitted text', async (t) => {
  const state = setup(t, async () => result)
  state.draftQuery.value = 'Boston'
  await state.submit()
  assert.equal(state.submittedQuery.value, 'Boston')
  state.draftQuery.value = 'NYC'
  assert.equal(state.response.value, null)
  assert.equal(state.submittedQuery.value, '')
  assert.equal(state.requestState.value, 'idle')
})

test('domain errors settle with a response; HTTP errors settle separately', async (t) => {
  const domain = { status: 'error', requirements: {}, errors: ['NO_RESULTS'] }
  let fail = false
  const state = setup(t, async () => {
    if (fail) throw new ApiError('Invalid travel requirements', 422)
    return domain
  })
  state.draftQuery.value = 'Atlantis'
  await state.submit()
  assert.equal(state.response.value.status, 'error')
  assert.equal(state.transportError.value, null)
  fail = true
  state.draftQuery.value = '0-day trip'
  await state.submit()
  assert.equal(state.requestState.value, 'settled')
  assert.equal(state.response.value, null)
  assert.equal(state.transportError.value.statusCode, 422)
})

test('reset aborts in-flight work and ignores late responses', async (t) => {
  let resolve
  let signal
  const state = setup(t, (_, supplied) => {
    signal = supplied
    return new Promise(done => { resolve = done })
  })
  state.draftQuery.value = 'Boston'
  const pending = state.submit()
  state.reset()
  assert.equal(signal.aborted, true)
  resolve(result)
  await pending
  assert.equal(state.response.value, null)
  assert.equal(state.requestState.value, 'idle')
  assert.equal(state.draftQuery.value, '')
})

import { presets, findScenario } from '../src/presets.ts'
import { demoTakeaway } from '../src/utils/demo.ts'

test('Phase E scenario selection clears results without submitting; edit and reset clear identity', async t => {
  let calls = 0
  const state = setup(t, async () => { calls++; return result })
  for (const preset of presets) {
    state.draftQuery.value = preset.query
    assert.equal(findScenario(state.draftQuery.value)?.id, preset.id)
    assert.equal(state.response.value, null)
    const before = calls
    await state.submit()
    assert.equal(calls, before + 1)
    assert.ok(state.response.value)
  }
  const before = calls
  state.draftQuery.value = presets[0].query
  assert.equal(calls, before)
  assert.equal(state.response.value, null)
  state.draftQuery.value += ' '
  assert.equal(findScenario(state.draftQuery.value), null)
  state.reset()
  assert.equal(findScenario(state.draftQuery.value), null)
  assert.equal(state.response.value, null)
  assert.equal(state.submittedQuery.value, '')
  assert.equal(state.transportError.value, null)
  assert.deepEqual(demoTakeaway(state.response.value), [])
})
