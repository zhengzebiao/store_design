import { request } from './client'
import type { SavePagePayload, SavePageResult } from '../domain/page'

export function savePage(payload: SavePagePayload) {
  return request<SavePageResult>('/api/store-design/pages/save', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
