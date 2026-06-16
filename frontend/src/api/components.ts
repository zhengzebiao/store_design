import { request } from './client'
import type { ComponentMeta } from '../domain/component'

export function getComponents() {
  return request<ComponentMeta[]>('/api/store-design/components')
}
