#!/bin/sh
set -eu

ENV_TARGET=/usr/share/nginx/html/micro-apps/store_design/env.js
cat > "$ENV_TARGET" <<EOF
window.__STORE_DESIGN_ENV__ = {
  API_BASE_URL: "${API_BASE_URL:-}",
  BASENAME: "${BASENAME:-/store_design}"
}
EOF
cp "$ENV_TARGET" /usr/share/nginx/html/env.js
