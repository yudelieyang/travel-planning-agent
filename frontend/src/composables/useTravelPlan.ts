import { getCurrentScope, onScopeDispose, ref, shallowRef, watch } from 'vue'
import { ApiError, planTravel } from '../api/travelApi.ts'
import type { PlanResponse } from '../types/travel.ts'

export function useTravelPlan(send: typeof planTravel = planTravel) {
  const draftQuery = ref('')
  const submittedQuery = ref('')
  const response = shallowRef<PlanResponse | null>(null)
  const requestState = ref<'idle' | 'submitting' | 'settled'>('idle')
  const transportError = shallowRef<ApiError | null>(null)
  let generation = 0
  let controller: AbortController | null = null

  function clearResult() {
    response.value = null
    transportError.value = null
    submittedQuery.value = ''
    requestState.value = 'idle'
  }

  // Editing or choosing another preset removes the previous result immediately.
  watch(draftQuery, () => {
    if (requestState.value !== 'submitting') clearResult()
  }, { flush: 'sync' })

  async function submit() {
    if (requestState.value === 'submitting' || !draftQuery.value.trim()) return
    const current = ++generation
    submittedQuery.value = draftQuery.value.trim()
    response.value = null
    transportError.value = null
    requestState.value = 'submitting'
    controller = new AbortController()
    try {
      const result = await send({ query: submittedQuery.value }, controller.signal)
      if (generation === current) response.value = result
    } catch (error) {
      if (generation === current) transportError.value = error instanceof ApiError
        ? error : new ApiError('The request could not be completed. Please try again.')
    } finally {
      if (generation === current) {
        requestState.value = 'settled'
        controller = null
      }
    }
  }

  function reset() {
    generation++
    controller?.abort()
    controller = null
    draftQuery.value = ''
    clearResult()
  }

  if (getCurrentScope()) onScopeDispose(() => { generation++; controller?.abort() })
  return { draftQuery, submittedQuery, response, requestState, transportError, submit, reset }
}
