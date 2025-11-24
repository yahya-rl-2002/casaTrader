import { useLocation } from "react-router-dom";
import { Bot, X, Loader2, Send, Maximize2, Minimize2 } from "lucide-react";
import { useSession } from "@/hooks/use-session";
import { useEffect, useMemo, useRef, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useToast } from "@/hooks/use-toast";
import { supabase } from "@/integrations/supabase/client";
import { cn } from "@/lib/utils";

type Msg = { role: "user" | "assistant"; content: string };

export function FloatingAssistantButton() {
  const { user, loading } = useSession();
  const location = useLocation();
  const { toast } = useToast();
  const [open, setOpen] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [messages, setMessages] = useState<Msg[]>([
    {
      role: "assistant",
      content:
        "Bonjour, je suis CasaTrader Bot. Posez-moi une question (marché, titres MASI, actualités)…",
    },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const endRef = useRef<HTMLDivElement | null>(null);

  const hasUserSpoken = useMemo(() => messages.some((m) => m.role === "user"), [messages]);

  const userInitials = useMemo(() => {
    const email = user?.email ?? "";
    const local = (email.split("@")[0] ?? "").replace(/[^A-Za-z0-9]/g, "");
    const up = local.toUpperCase();
    if (up.length >= 2) return up.slice(0, 2);
    if (up.length === 1) return up + "_";
    return "US";
  }, [user?.email]);

  useEffect(() => {
    if (open) endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [open, messages]);

  if (loading || !user) return null;
  if (location.pathname === "/assistant") return null;

  async function send(override?: string) {
    const q = (override ?? input).trim();
    if (!q || sending) return;
    setInput(override ? "" : "");
    setSending(true);
    const next = [...messages, { role: "user" as const, content: q }];
    setMessages(next);
    try {
      const { data, error } = await supabase.functions.invoke("ai-chat", {
        body: { messages: next, provider: "openai" },
      });
      if (error) throw error;
      if (!data?.success) {
        const details = (data?.details as string | undefined) ?? "";
        throw new Error((data?.error as string) + (details ? ` — ${details.slice(0, 180)}` : ""));
      }
      const content: string = (data?.content as string) ?? "(aucune réponse)";
      setMessages((m) => [...m, { role: "assistant", content }]);
    } catch (err) {
      toast({ title: "Erreur", description: err instanceof Error ? err.message : "Echec de la requête", variant: "destructive" });
    } finally {
      setSending(false);
    }
  }

  function handleSuggestion(text: string) {
    setInput(text);
    void send(text);
  }

  return (
    <>
      {/* Bouton flottant */}
      <button
        aria-label="Ouvrir l'assistant"
        className={cn(
          "fixed bottom-5 right-5 z-50 h-[52px] w-[52px] rounded-full text-primary-foreground shadow-lg hover:shadow-xl transition flex items-center justify-center",
          "bg-gradient-to-br from-primary to-purple-600",
          !open && "motion-safe:animate-bot-jump hover:animate-none active:animate-none"
        )}
        onClick={() => setOpen((v) => !v)}
      >
        {open ? <X className="w-6 h-6" /> : <Bot className="w-6 h-6" />}
      </button>

      {/* Panneau de chat */}
      {open && (
        <div
          className={cn(
            "fixed bottom-24 right-5 z-50 max-w-[92vw]",
            expanded ? "w-[540px]" : "w-[360px] md:w-[400px]"
          )}
        >
          <Card className={cn(
            "rounded-2xl border shadow-2xl overflow-hidden",
            "bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60"
          )}>
            <div className="h-1 w-full bg-gradient-to-r from-primary via-purple-500 to-pink-500" />
            <CardHeader className="py-3 flex flex-row items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-full bg-gradient-to-br from-primary to-purple-600 text-primary-foreground flex items-center justify-center shadow">
                  <Bot className="w-[18px] h-[18px]" />
                </div>
                <div>
                  <CardTitle className="text-sm leading-tight">CasaTrader Bot</CardTitle>
                  <div className="flex items-center gap-2">
                    <div className="flex items-center gap-1 text-xs text-muted-foreground">
                      <span className="inline-block h-2 w-2 rounded-full bg-emerald-500" />
                      En ligne
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-1">
                <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => setExpanded((v) => !v)} aria-label={expanded ? "Réduire" : "Agrandir"}>
                  {expanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
                </Button>
                <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => setOpen(false)} aria-label="Fermer">
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </CardHeader>

            <CardContent className={cn("pt-2", expanded ? "pb-4" : "pb-2")}> 
              <div className={cn(expanded ? "h-[500px]" : "h-[420px]", "flex flex-col")}> 
                <ScrollArea className="flex-1 pr-1">
                  <div className="space-y-3">
                    {messages.map((m, i) => (
                      <div key={i} className={cn("flex items-start gap-3", m.role === "user" ? "justify-end" : "justify-start")}> 
                        {m.role === "assistant" && (
                          <Avatar className="h-7 w-7">
                            <AvatarFallback className="bg-primary/10 text-primary">B</AvatarFallback>
                          </Avatar>
                        )}
                        <div
                          className={cn(
                            "max-w-[85%] rounded-2xl px-3 py-2 text-sm",
                            m.role === "user"
                              ? "bg-gradient-to-r from-primary to-purple-600 text-primary-foreground shadow"
                              : "bg-muted text-foreground"
                          )}
                        >
                          {m.role === "assistant" ? (
                            <div className="prose prose-sm max-w-none prose-headings:scroll-mt-24 prose-p:leading-relaxed prose-a:text-primary hover:prose-a:underline">
                              <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
                            </div>
                          ) : (
                            m.content
                          )}
                        </div>
                        {m.role === "user" && (
                          <Avatar className="h-7 w-7">
                            <AvatarFallback className="bg-primary text-primary-foreground">{userInitials}</AvatarFallback>
                          </Avatar>
                        )}
                      </div>
                    ))}

                    {sending && (
                      <div className="flex items-start gap-3">
                        <Avatar className="h-7 w-7">
                          <AvatarFallback className="bg-primary/10 text-primary">B</AvatarFallback>
                        </Avatar>
                        <div className="rounded-2xl px-3 py-2 text-sm bg-muted text-foreground inline-flex items-center gap-2">
                          <Loader2 className="w-4 h-4 animate-spin" />
                          Rédaction en cours…
                        </div>
                      </div>
                    )}

                    <div ref={endRef} />
                  </div>
                </ScrollArea>

                {/* Suggestions rapides */}
                {!hasUserSpoken && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {[
                      "Résumé du marché aujourd'hui au Maroc",
                      "Analyse d'ATW (Attijariwafa Bank)",
                      "Impact d'une hausse du taux directeur",
                      "Idées d'alertes sur le MASI",
                    ].map((s) => (
                      <Button key={s} size="sm" variant="outline" className="h-7 text-xs" onClick={() => handleSuggestion(s)}>
                        {s}
                      </Button>
                    ))}
                  </div>
                )}

                {/* Composer */}
                <div className="mt-3 flex items-end gap-2">
                  <Textarea
                    placeholder={sending ? "Envoi en cours…" : "Rédigez votre message…"}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault();
                        void send();
                      }
                    }}
                    disabled={sending}
                    className="min-h-[40px] max-h-28 resize-none"
                  />
                  <Button onClick={() => void send()} disabled={sending || !input.trim()} className="h-[40px] px-3">
                    {sending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                  </Button>
                </div>

                <p className="mt-2 text-[10px] text-muted-foreground">
                  Les réponses sont générées par IA. Ceci n'est pas un conseil en investissement.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </>
  );
}
