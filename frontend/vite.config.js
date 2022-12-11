import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import WindiCSS from 'vite-plugin-windicss'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        WindiCSS(),
    ],
    server: {
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000/',   // 10.193.48.101  10.193.8.66   10.128.54.139
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ''),
            },
        }
    }

})
