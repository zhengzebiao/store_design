import { StrictMode } from 'react'
import { createRoot, type Root } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { App as AntdApp, ConfigProvider } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import App from './app/App'
import { getRuntimeConfig, setRuntimeConfig } from './config/runtime'
import './styles/global.less'

type MicroAppProps = {
  container?: HTMLElement
  basename?: string
  apiBaseUrl?: string
}

let root: Root | null = null
let queryClient: QueryClient | null = null

function render(props: MicroAppProps = {}) {
  setRuntimeConfig({
    basename: props.basename,
    apiBaseUrl: props.apiBaseUrl,
  })

  const container = props.container?.querySelector('#root') ?? document.getElementById('root')
  if (!container) {
    throw new Error('store_design root container not found')
  }

  queryClient = new QueryClient()
  root = createRoot(container)
  root.render(
    <StrictMode>
      <ConfigProvider locale={zhCN}>
        <AntdApp>
          <QueryClientProvider client={queryClient}>
            <BrowserRouter
              basename={getRuntimeConfig().basename}
              future={{ v7_relativeSplatPath: true, v7_startTransition: true }}
            >
              <App />
            </BrowserRouter>
          </QueryClientProvider>
        </AntdApp>
      </ConfigProvider>
    </StrictMode>,
  )
}

if (!window.__POWERED_BY_QIANKUN__) {
  render()
}

export async function bootstrap() {}

export async function mount(props: MicroAppProps) {
  render(props)
}

export async function unmount() {
  root?.unmount()
  root = null
  queryClient?.clear()
  queryClient = null
}
