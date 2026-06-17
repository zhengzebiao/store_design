import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'
import type { DesignComponent } from '../domain/component'
import type { StoreDesignPage } from '../domain/page'
import { createEmptyPage } from '../domain/factory'

type EditorMode = 'create' | 'edit' | 'copy'
type MoveDirection = 'up' | 'down'

type EditorState = {
  mode: EditorMode
  route_id: string
  page: StoreDesignPage
  selectedComponentId?: string
  setMode: (mode: EditorMode) => void
  setRouteId: (routeId: string) => void
  setPage: (page: StoreDesignPage) => void
  addComponent: (component: DesignComponent) => void
  selectComponent: (id?: string) => void
  removeComponent: (id: string) => void
  copyComponent: (id: string) => void
  moveComponent: (id: string, direction: MoveDirection) => void
  updatePageName: (pageName: string) => void
  updateSelectedTitle: (title: string) => void
  updateSelectedRemoteData: (key: string, value: unknown) => void
}

function setByPath(target: Record<string, unknown>, path: string, value: unknown) {
  const keys = path.split('.').filter(Boolean)
  if (keys.length === 0) return

  let current = target
  keys.slice(0, -1).forEach((key) => {
    const next = current[key]
    if (!next || typeof next !== 'object' || Array.isArray(next)) {
      current[key] = {}
    }
    current = current[key] as Record<string, unknown>
  })
  current[keys[keys.length - 1]] = value
}

function cloneComponent(component: DesignComponent): DesignComponent {
  return {
    ...component,
    id: `${component.component_key}_${Date.now()}`,
    component_title: `${component.component_title} 副本`,
    remote_data: structuredClone(component.remote_data),
    tasks: component.tasks ? structuredClone(component.tasks) : undefined,
  }
}

export const useEditorStore = create<EditorState>()(
  immer((set) => ({
    mode: 'create',
    route_id: '',
    page: createEmptyPage(),
    setMode: (mode) => set((state) => { state.mode = mode }),
    setRouteId: (routeId) => set((state) => { state.route_id = routeId }),
    setPage: (page) => set((state) => { state.page = page }),
    addComponent: (component) => set((state) => { state.page.datas.push(component) }),
    selectComponent: (id) => set((state) => { state.selectedComponentId = id }),
    removeComponent: (id) => set((state) => {
      state.page.datas = state.page.datas.filter((item) => item.id !== id)
      if (state.selectedComponentId === id) {
        state.selectedComponentId = undefined
      }
    }),
    copyComponent: (id) => set((state) => {
      const index = state.page.datas.findIndex((item) => item.id === id)
      if (index < 0) return
      const copied = cloneComponent(state.page.datas[index])
      state.page.datas.splice(index + 1, 0, copied)
      state.selectedComponentId = copied.id
    }),
    moveComponent: (id, direction) => set((state) => {
      const index = state.page.datas.findIndex((item) => item.id === id)
      const nextIndex = direction === 'up' ? index - 1 : index + 1
      if (index < 0 || nextIndex < 0 || nextIndex >= state.page.datas.length) return
      const [component] = state.page.datas.splice(index, 1)
      state.page.datas.splice(nextIndex, 0, component)
      state.selectedComponentId = id
    }),
    updatePageName: (pageName) => set((state) => { state.page.page_name = pageName }),
    updateSelectedTitle: (title) => set((state) => {
      const selected = state.page.datas.find((item) => item.id === state.selectedComponentId)
      if (selected) {
        selected.component_title = title
      }
    }),
    updateSelectedRemoteData: (key, value) => set((state) => {
      const selected = state.page.datas.find((item) => item.id === state.selectedComponentId)
      if (selected) {
        setByPath(selected.remote_data, key, value)
      }
    }),
  })),
)
