FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY docker-entrypoint.sh /docker-entrypoint.d/99-store-design-env.sh
COPY --from=builder /app/dist /usr/share/nginx/html/micro-apps/store_design
EXPOSE 80
