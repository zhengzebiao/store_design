import { request, requestPage } from './client'
import type { StoreTemplate, TemplateListParams } from '../domain/template'
import type { StoreDesignPage } from '../domain/page'

export function getTemplates(params: TemplateListParams) {
  const search = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== '') {
      search.set(key, String(value))
    }
  })
  return requestPage<StoreTemplate>(`/api/store-design/templates?${search.toString()}`)
}

export function getTemplateDetail(id: string | number) {
  return request<StoreDesignPage>(`/api/store-design/templates/${id}`)
}

export function useTemplate(id: string | number, companyId: string | number) {
  return request(`/api/store-design/templates/${id}/use`, {
    method: 'POST',
    body: JSON.stringify({ company_id: companyId }),
  })
}

export function deleteTemplate(id: string | number, companyId: string | number) {
  return request(`/api/store-design/templates/${id}?company_id=${companyId}`, {
    method: 'DELETE',
  })
}
