import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  build: {
    outDir: 'public', // Specify the desired output directory (e.g., 'public')
    assetsDir: 'assets', // Specify the directory for your assets (e.g., 'assets')
    rollupOptions: {
      output: {
        entryFileNames: 'index.js', // Specify the name of the JavaScript bundle
        assetFileNames: (assetInfo) => {
          if (assetInfo.name === 'style.css') return 'custom.css';
          return assetInfo.name;
        },
      },
    },
  },
})
