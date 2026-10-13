import fs from "node:fs"
import path from "node:path"
import tailwindcss from "@tailwindcss/vite"
import { tanstackRouter } from "@tanstack/router-plugin/vite"
import react from "@vitejs/plugin-react-swc"
import { defineConfig } from "vite"

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    outDir: process.env.VITE_OUT_DIR || "dist",
    emptyOutDir: true,
  },
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "./src"),
    },
  },
  plugins: [
    tanstackRouter({
      target: "react",
      autoCodeSplitting: true,
    }),
    react(),
    tailwindcss(),
    {
      name: "spa-fallback-200",
      closeBundle() {
        const outDir = path.resolve(
          import.meta.dirname,
          process.env.VITE_OUT_DIR || "dist",
        )
        const indexPath = path.join(outDir, "index.html")
        const fallbackPath = path.join(outDir, "200.html")
        if (fs.existsSync(indexPath)) {
          fs.copyFileSync(indexPath, fallbackPath)
        }
      },
    },
  ],
})
