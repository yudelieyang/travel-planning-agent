import test from 'node:test'
import assert from 'node:assert/strict'
import { ApiError, planTravel } from '../src/api/travelApi.ts'

test('sends only query and preserves HTTP 200 domain errors', async (t) => {
  const body = { status: 'error', requirements: {}, execution: null, errors: ['search_hotels: NO_RESULTS'] }
  const fetchMock = t.mock.method(globalThis, 'fetch', async (url, options) => {
    assert.equal(url, '/api/v1/travel/plan')
    assert.equal(options.method, 'POST')
    assert.equal(options.headers['Content-Type'], 'application/json')
    assert.deepEqual(JSON.parse(options.body), { query: 'Plan a trip.' })
    return Response.json(body)
  })
  assert.deepEqual(await planTravel({ query: 'Plan a trip.', unexpected: true }), body)
  assert.equal(fetchMock.mock.callCount(), 1)
})

for (const status of ['success', 'needs_clarification']) {
  test(`preserves ${status} and nullable execution/budget values`, async (t) => {
    const body = { status, requirements: {}, execution: null, budget: null }
    t.mock.method(globalThis, 'fetch', async () => Response.json(body))
    assert.deepEqual(await planTravel({ query: 'Request' }), body)
  })
}

test('normalizes FastAPI string details', async (t) => {
  t.mock.method(globalThis, 'fetch', async () => Response.json(
    { detail: 'Invalid or inconsistent travel requirements' }, { status: 422 },
  ))
  await assert.rejects(planTravel({ query: '0 days' }), error => {
    assert.ok(error instanceof ApiError)
    assert.equal(error.statusCode, 422)
    assert.equal(error.message, 'Invalid or inconsistent travel requirements')
    return true
  })
})

test('validation arrays expose messages, not inputs or context', async (t) => {
  t.mock.method(globalThis, 'fetch', async () => Response.json({ detail: [
    { msg: 'String should have at most 2000 characters', input: 'PRIVATE_INPUT', ctx: { secret: 'PRIVATE_CTX' } },
  ] }, { status: 422 }))
  await assert.rejects(planTravel({ query: 'Request' }), error => {
    assert.equal(error.message, 'String should have at most 2000 characters')
    assert.doesNotMatch(error.message, /PRIVATE/)
    return true
  })
})

test('non-JSON HTTP errors never display HTML or stack traces', async (t) => {
  t.mock.method(globalThis, 'fetch', async () => new Response('<html>PRIVATE_STACK_TRACE</html>', { status: 503 }))
  await assert.rejects(planTravel({ query: 'Request' }), error => {
    assert.equal(error.statusCode, 503)
    assert.match(error.message, /HTTP 503/)
    assert.doesNotMatch(error.message, /html|PRIVATE/)
    return true
  })
})

test('normalizes connection failure', async (t) => {
  t.mock.method(globalThis, 'fetch', async () => { throw new TypeError('PRIVATE_NETWORK_DETAIL') })
  await assert.rejects(planTravel({ query: 'Request' }), error => {
    assert.equal(error.statusCode, undefined)
    assert.match(error.message, /Could not reach the backend/)
    assert.doesNotMatch(error.message, /PRIVATE/)
    return true
  })
})

test('rejects malformed successful envelopes', async (t) => {
  t.mock.method(globalThis, 'fetch', async () => Response.json({ status: 'unknown' }))
  await assert.rejects(planTravel({ query: 'Request' }), /unexpected response/)
})
