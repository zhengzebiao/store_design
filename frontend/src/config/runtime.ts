type RuntimeConfig = {
  apiBaseUrl: string
  basename: string
}

const config: RuntimeConfig = {
  apiBaseUrl: window.__STORE_DESIGN_ENV__?.API_BASE_URL || import.meta.env.VITE_API_BASE_URL || '',
  basename: window.__STORE_DESIGN_ENV__?.BASENAME || import.meta.env.VITE_BASENAME || '/store_design',
}

export function setRuntimeConfig(next: { apiBaseUrl?: string; basename?: string }) {
  if (next.apiBaseUrl) {
    config.apiBaseUrl = next.apiBaseUrl
  }
  if (next.basename) {
    config.basename = next.basename
  }
}

export function getRuntimeConfig() {
  return config
}
