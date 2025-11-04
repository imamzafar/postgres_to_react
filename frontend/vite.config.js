import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const apiProxy = env.VITE_USE_PROXY === "true";

  return {
    plugins: [react()],
    server: {
      port: 5173,
      proxy: apiProxy
        ? {
            "/api": {
              target: env.VITE_API_PROXY_TARGET ?? "http://localhost:8000",
              changeOrigin: true,
            },
          }
        : undefined,
    },
    preview: {
      port: 4173,
    },
  };
});
