import type { NextConfig } from "next";

// All /api/* calls are proxied to the local Python bridge (scripts/web_api.py).
const API_ORIGIN = process.env.POLICY_API_ORIGIN ?? "http://127.0.0.1:8790";

const nextConfig: NextConfig = {
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${API_ORIGIN}/:path*` }];
  },
  // Live model turns and live replays can take well over the 30s proxy default.
  experimental: { proxyTimeout: 600_000 },
};

export default nextConfig;
