import { getRuntimeConfig } from '../config/runtime'

export type ApiResponse<T> = {
  success: boolean
  data?: T
  error_code?: string
  error_info?: string
  details?: unknown
}

export type PageResponse<T> = ApiResponse<T[]> & {
  current_page: number
  limit: number
  total: number
}

export class ApiError extends Error {
  code?: string
  details?: unknown

  constructor(message: string, code?: string, details?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.code = code
    this.details = details
  }
}

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const { apiBaseUrl } = getRuntimeConfig()
  const response = await fetch(`${apiBaseUrl}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...init?.headers,
    },
    ...init,
  })

  const payload = (await response.json()) as ApiResponse<T>
  if (!response.ok || !payload.success) {
    throw new ApiError(payload.error_info || response.statusText, payload.error_code, payload.details)
  }

  return payload.data as T
}

export async function requestPage<T>(path: string): Promise<PageResponse<T>> {
  const { apiBaseUrl } = getRuntimeConfig()
  const response = await fetch(`${apiBaseUrl}${path}`)
  const payload = (await response.json()) as PageResponse<T>
  if (!response.ok || !payload.success) {
    throw new ApiError(payload.error_info || response.statusText, payload.error_code, payload.details)
  }
  return payload
}
