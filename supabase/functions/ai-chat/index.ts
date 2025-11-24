// Perplexity AI Chat proxy (Supabase Edge Function)
// Expects secret: PERPLEXITY_API_KEY

import { createClient } from "https://esm.sh/@supabase/supabase-js@2.39.3";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

type ChatMessage = { role: "system" | "user" | "assistant"; content: string };

function jsonResponse(payload: unknown, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }
  try {
    const apiKey = Deno.env.get("PERPLEXITY_API_KEY");
    if (!apiKey) return jsonResponse({ success: false, error: "Missing PERPLEXITY_API_KEY" }, 200);

    const { messages, model, temperature, provider } = (await req.json().catch(() => ({}))) as {
      messages?: ChatMessage[];
      model?: string;
      temperature?: number;
      provider?: "perplexity" | "openai";
    };
    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return jsonResponse({ error: "Provide messages: ChatMessage[]" }, 400);
    }

    // Perplexity current public models: sonar-*-online / sonar-*-chat
    // Provider routing (default perplexity; openai also supported)
    if (provider === "openai") {
      const openaiKey = Deno.env.get("OPENAI_API_KEY");
      if (!openaiKey) return jsonResponse({ success: false, error: "Missing OPENAI_API_KEY" }, 200);
      const OPENAI_DEFAULT = model || "gpt-4o-mini";
      const OPENAI_FALLBACKS = ["gpt-4o-mini", "gpt-4o" , "gpt-3.5-turbo"];
      const tryOrder = [OPENAI_DEFAULT, ...OPENAI_FALLBACKS.filter((m) => m !== OPENAI_DEFAULT)];

      // Build finance-focused context from latest articles (if available)
      async function buildContext(question: string): Promise<string> {
        try {
          const sbUrl = Deno.env.get("SUPABASE_URL") ?? Deno.env.get("PROJECT_URL");
          const sbKey = Deno.env.get("SERVICE_ROLE_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
          if (!sbUrl || !sbKey) return "";
          const sb = createClient(sbUrl, sbKey);
          const kw = question.toLowerCase().split(/[^\p{L}\p{N}]+/u).filter((w) => w.length >= 3).slice(0, 6);
          // Récupère les derniers articles et filtre côté code si mots-clés présents
          const { data } = await sb
            .from('articles')
            .select('title,source,description,content,source_url,published_at')
            .order('published_at', { ascending: false })
            .limit(30);
          const items = Array.isArray(data) ? data : [];
          const scored = items.map((it: any) => {
            const text = `${it.title ?? ''} ${it.description ?? ''} ${it.content ?? ''}`.toLowerCase();
            const score = kw.reduce((s, k) => s + (text.includes(k) ? 1 : 0), 0) + (/(casa|casablanca|masi|bourse)/i.test(text) ? 1 : 0);
            return { it, score };
          }).sort((a,b) => b.score - a.score);
          const top = (scored.length ? scored.slice(0, 8) : items.slice(0, 8)).map((x: any) => x.it ?? x);
          if (!top.length) return "";
          const bullets = top.map((a: any, i: number) => `[$${i+1}] ${a.source ?? ''} — ${a.title ?? ''} (${a.published_at ?? ''})\n${(a.description ?? a.content ?? '').toString().slice(0,240)}\nURL: ${a.source_url}`);
          return bullets.join("\n\n");
        } catch {
          return "";
        }
      }

      const lastUser = [...messages].reverse().find((m) => m.role === 'user')?.content ?? '';
      const context = await buildContext(lastUser);

      const system = `Tu es un analyste financier senior spécialisé sur la Bourse de Casablanca (MASI) et les marchés internationaux.\n\nConsignes:\n- Réponds en français par défaut (utilise la langue de l'utilisateur si différente).\n- Structure la réponse: 1) Vue d'ensemble, 2) Points clés (puces), 3) Impacts marché, 4) Risques, 5) Prochaines étapes.\n- Utilise le contexte fourni (actualités/infos ci-dessous) quand pertinent et cite les sources sous forme [#].\n- Si le contexte est insuffisant, indique-le et propose des pistes.\n- Reste factuel. Ajoute la mention: Ceci n'est pas un conseil en investissement.`;

      for (const m of tryOrder) {
        const body = { model: m, messages: [{ role: 'system', content: system }, ...(context ? [{ role: 'user', content: `CONTEXTE (sources récentes):\n${context}` }] : []), ...messages], temperature: typeof temperature === "number" ? temperature : 0.2, stream: false };
        const resp = await fetch("https://api.openai.com/v1/chat/completions", {
          method: "POST",
          headers: { "Content-Type": "application/json", Authorization: `Bearer ${openaiKey}` },
          body: JSON.stringify(body),
        });
        const text = await resp.text().catch(() => "");
        if (resp.ok) {
          // OpenAI returns {choices:[{message:{content}}]}
          const data = JSON.parse(text);
          const content: string | undefined = data?.choices?.[0]?.message?.content;
          const usage = data?.usage;
          return jsonResponse({ success: true, content, usage, model: m, provider: "openai" }, 200);
        }
        if (resp.status === 400 && /model/i.test(text)) continue;
        return jsonResponse({ success: false, error: `OpenAI error ${resp.status}`, details: text }, 200);
      }
      return jsonResponse({ success: false, error: "All OpenAI model attempts failed" }, 200);
    }

    // Try to fetch allowed models for this key
    async function listPerplexityModels(): Promise<string[] | null> {
      try {
        const res = await fetch("https://api.perplexity.ai/models", {
          method: "GET",
          headers: { Authorization: `Bearer ${apiKey}` },
        });
        if (!res.ok) return null;
        const data = await res.json();
        const ids: string[] = Array.isArray(data?.data)
          ? data.data.map((m: any) => m?.id).filter((x: any) => typeof x === "string")
          : [];
        return ids.length ? ids : null;
      } catch {
        return null;
      }
    }

    // Build candidate list: requested → allowed by API → sensible defaults
    const defaults = [
      "sonar-small-online",
      "sonar-medium-online",
      "sonar-large-online",
      "sonar-small-chat",
      "sonar-medium-chat",
      "sonar-large-chat",
      "pplx-7b-online",
      "pplx-70b-online",
      "pplx-7b-chat",
      "pplx-70b-chat",
    ];
    const listed = (await listPerplexityModels()) ?? [];
    const CANDIDATES = [
      ...(model ? [model] : []),
      ...listed.filter((m) => /sonar-.*-online/i.test(m)),
      ...listed.filter((m) => /sonar-.*-chat/i.test(m)),
      ...listed, // any remaining ids
      ...defaults,
    ].filter((m, i, arr) => typeof m === "string" && arr.indexOf(m) === i) as string[];

    async function callModel(m: string) {
      const body = {
        model: m,
        messages,
        temperature: typeof temperature === "number" ? temperature : 0.2,
        stream: false,
      };
      const resp = await fetch("https://api.perplexity.ai/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify(body),
      });
      return resp;
    }

    // Try requested model, else default, with fallbacks when model invalid
    const tryOrder = CANDIDATES;

    let lastText = "";
    for (const m of tryOrder) {
      const resp = await callModel(m);
      const text = await resp.text().catch(() => "");
      if (resp.ok) {
        const data = JSON.parse(text);
        const content: string | undefined = data?.choices?.[0]?.message?.content;
        const usage = data?.usage;
        return jsonResponse({ success: true, content, usage, model: m }, 200);
      }
      lastText = text;
      if (resp.status === 400 && /Invalid model/i.test(text)) {
        continue; // try next fallback model
      }
      // Other upstream error, don't retry through the list
      return jsonResponse({ success: false, error: `Upstream error ${resp.status}`, details: text }, 200);
    }
    return jsonResponse({ success: false, error: "All model attempts failed", details: lastText }, 200);
  } catch (err) {
    return jsonResponse({ success: false, error: err instanceof Error ? err.message : "Unknown error" }, 200);
  }
});
