import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: 3000,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        ws: true,
        rewrite: (path) => path,
        configure: (proxy, options) => {
          proxy.on("proxyRes", (proxyRes, req, res) => {
            // Ensure streaming responses aren't buffered
            if (proxyRes.headers["content-type"] === "text/event-stream") {
              proxyRes.removeHeader("content-length");
              proxyRes.setHeader("transfer-encoding", "chunked");
              proxyRes.setHeader("cache-control", "no-cache");
            }
          });
        },
      },
    },
  },
  build: {
    outDir: "dist",
  },
});
