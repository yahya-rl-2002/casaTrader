import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const tunnelHost = process.env.VITE_TUNNEL_HOST;

  return {
    server: {
      host: true, // expose on network (0.0.0.0)
      port: 8080,
      // Proxy pour rediriger les appels API vers le backend Fear & Greed
      proxy: {
        '/api/v1': {
          target: 'http://127.0.0.1:8001',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path,
        },
      },
      // En local (pas de VITE_TUNNEL_HOST), on évite le HMR distant
      // et on active un watch en polling (disques externes/macOS)
      ...(tunnelHost
        ? {
            allowedHosts: [tunnelHost],
            hmr: {
              host: tunnelHost,
              protocol: "wss",
              clientPort: 443,
            },
          }
        : {
            watch: { usePolling: true, interval: 200 },
          }),
    },
    plugins: [react(), mode === "development" && tunnelHost && componentTagger()].filter(Boolean),
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
      dedupe: ["react", "react-dom"],
    },
    optimizeDeps: {
      include: ["react", "react-dom", "@tanstack/react-query"],
    },
  };
});
