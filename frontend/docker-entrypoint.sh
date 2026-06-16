#!/bin/sh
set -eu

cat > /usr/share/nginx/html/env.js <<EOF
window.__STORE_DESIGN_ENV__ = {
  API_BASE_URL: "${API_BASE_URL:-}",
  BASENAME: "${BASENAME:-/store_design}"
}
EOF
