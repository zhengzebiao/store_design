import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'
import type { DesignComponent } from '../domain/component'
import type { StoreDesignPage } from '../domain/page'
import { createEmptyPage } from '../domain/factory'

type EditorMode = 'create' | 'edit' | 'copy'

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
  updatePageName: (pageName: string) => void
  updateSelectedTitle: (title: string) => void
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
    updatePageName: (pageName) => set((state) => { state.page.page_name = pageName }),
    updateSelectedTitle: (title) => set((state) => {
      const selected = state.page.datas.find((item) => item.id === state.selectedComponentId)
      if (selected) {
        selected.component_title = title
        selected.remote_data = { ...selected.remote_data, title }
      }
    }),
  })),
)
