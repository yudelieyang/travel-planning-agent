import type { PlanRequest, PlanResponse } from '../types/travel.ts'

export class ApiError extends Error {
  readonly statusCode?: number
  constructor(message: string, statusCode?: number) {
    super(message)
    this.name = 'ApiError'
    this.statusCode = statusCode
  }
}

function record(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
}

function messageText(value: unknown): string | null {
  if (typeof value !== 'string' || /<[^>]*>|Traceback|\n\s+at\s/.test(value)) return null
  return value.replace(/\s+/g, ' ').trim().slice(0, 300) || null
}

function errorMessage(body: unknown, status: number): string {
  const detail = record(body) ? body.detail : null
  const text = messageText(detail)
  if (text) return text
  if (Array.isArray(detail)) {
    const messages = detail.flatMap(item => {
      const message = record(item) ? messageText(item.msg) : null
      return message ? [message] : []
    })
    if (messages.length) return [...new Set(messages)].slice(0, 3).join(' ')
  }
  return `The backend could not complete the request (HTTP ${status}). Please try again.`
}

export async function planTravel(request: PlanRequest, signal?: AbortSignal): Promise<PlanResponse> {
  let response: Response
  try {
    response = await fetch('/api/v1/travel/plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ query: request.query }),
      signal,
    })
  } catch {
    throw new ApiError('Could not reach the backend. Check the local servers and try again.')
  }

  let body: unknown
  try { body = await response.json() } catch { body = null }
  if (!response.ok) throw new ApiError(errorMessage(body, response.status), response.status)
  // Envelope check only; the backend remains the authority for domain validation.
  if (!record(body) || !['success', 'needs_clarification', 'error'].includes(String(body.status))
      || !record(body.requirements)) {
    throw new ApiError('The backend returned an unexpected response. Please try again.', response.status)
  }
  return body as unknown as PlanResponse
}
