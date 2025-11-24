import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const url = new URL(req.url);
    const target = url.searchParams.get("url");
    if (!target) {
      return new Response("Missing url parameter", { status: 400, headers: corsHeaders });
    }

    // Validate URL
    let parsed: URL;
    try {
      parsed = new URL(target);
    } catch {
      return new Response("Invalid url", { status: 400, headers: corsHeaders });
    }

    const origin = `${parsed.protocol}//${parsed.host}`;
    const upstream = await fetch(parsed.toString(), {
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3",
        "Referer": origin,
      },
    });

    if (!upstream.ok) {
      return new Response(`Upstream error: ${upstream.status}`, { status: upstream.status, headers: corsHeaders });
    }

    const headers = new Headers(corsHeaders);
    const contentType = upstream.headers.get("content-type") ?? "application/octet-stream";
    headers.set("Content-Type", contentType);
    headers.set("Cache-Control", upstream.headers.get("cache-control") ?? "public, max-age=3600");

    return new Response(upstream.body, { status: 200, headers });
  } catch (error) {
    console.error("image proxy error", error);
    return new Response("Internal error", { status: 500, headers: corsHeaders });
  }
});
