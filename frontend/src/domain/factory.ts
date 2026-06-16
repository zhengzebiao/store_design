import type { ComponentMeta, DesignComponent } from './component'
import type { StoreDesignPage } from './page'

export function createEmptyPage(): StoreDesignPage {
  return {
    id: '',
    diy_id: '',
    company_id: 3,
    type: 'home_page',
    page_name: '首页装修',
    datas: [],
    other_company_show: 0,
    page_info: {},
    member_level: [],
    level: [],
    status: 1,
    page_sort: 2,
    page_scene: 2,
    top_id: {},
    foot_type: 1,
    foot_id: {},
    page_type: '2',
  }
}

export function createComponentFromMeta(meta: ComponentMeta): DesignComponent {
  return {
    id: `${meta.component_key}_${Date.now()}`,
    component_key: meta.component_key,
    component_title: meta.name,
    template_id: meta.tpl_id || meta.templates[0]?.id || '',
    remote_data: meta.default_data || {},
  }
}
