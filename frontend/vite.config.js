import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({
    base: '/micro-apps/store_design/',
    plugins: [react()],
    server: {
        port: 5174,
        headers: {
            'Access-Control-Allow-Origin': '*',
        },
        proxy: {
            '/api': 'http://localhost:8000',
            '/health': 'http://localhost:8000',
        },
    },
    build: {
        target: 'es2018',
        outDir: 'dist',
    },
});
