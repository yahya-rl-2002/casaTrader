import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, Eye, EyeOff, Mail, Lock, Facebook } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

const authSchema = z.object({
  email: z.string().trim().email({ message: "Email invalide" }),
  password: z.string().min(6, { message: "Au moins 6 caractères" }).max(100, { message: "Trop long" }),
});

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  const form = useForm<z.infer<typeof authSchema>>({
    resolver: zodResolver(authSchema),
    defaultValues: { email: "", password: "" },
    mode: "onChange",
  });

  // Si session déjà active → redirection
  useEffect(() => {
    const init = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      if (session) navigate("/");
    };
    init();
    const { data } = supabase.auth.onAuthStateChange((_event, session) => {
      if (session) navigate("/");
    });
    return () => data.subscription.unsubscribe();
  }, [navigate]);

  const handleSubmit = async (values: z.infer<typeof authSchema>) => {
    setLoading(true);
    try {
      if (isLogin) {
        const { error } = await supabase.auth.signInWithPassword({
          email: values.email,
          password: values.password,
        });
        if (error) {
          toast({
            title: "Connexion impossible",
            description: error.message.includes("Invalid") ? "Email ou mot de passe incorrect" : error.message,
            variant: "destructive",
          });
        } else {
          toast({ title: "Bienvenue", description: "Connexion réussie" });
        }
      } else {
        const redirectUrl = `${window.location.origin}/`;
        const { error } = await supabase.auth.signUp({
          email: values.email,
          password: values.password,
          options: { emailRedirectTo: redirectUrl },
        });
        if (error) {
          toast({
            title: "Inscription impossible",
            description: error.message.includes("already registered") ? "Un compte existe déjà avec cet email" : error.message,
            variant: "destructive",
          });
        } else {
          toast({ title: "Inscription réussie", description: "Bienvenue sur CasaTrader" });
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async () => {
    const email = form.getValues("email");
    if (!email) {
      toast({ title: "Email requis", description: "Renseignez votre email pour réinitialiser le mot de passe" });
      return;
    }
    setLoading(true);
    try {
      const redirectUrl = `${window.location.origin}/auth`;
      const { error } = await supabase.auth.resetPasswordForEmail(email, { redirectTo: redirectUrl });
      if (error) throw error;
      toast({ title: "Email envoyé", description: "Vérifiez votre boîte mail" });
    } catch (e) {
      toast({ title: "Erreur", description: e instanceof Error ? e.message : "Impossible d'envoyer l'email", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  const handleOAuth = async (provider: "google" | "facebook") => {
    setLoading(true);
    try {
      const redirectUrl = `${window.location.origin}/`;
      const { error } = await supabase.auth.signInWithOAuth({ provider, options: { redirectTo: redirectUrl } });
      if (error) throw error;
    } catch (e) {
      toast({ title: "Erreur OAuth", description: e instanceof Error ? e.message : "Connexion OAuth impossible", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="grid md:grid-cols-2 min-h-screen">
        {/* Panneau visuel (desktop) */}
        <div className="hidden md:flex relative items-center justify-center p-10 overflow-hidden">
          {/* Background image floue + overlay */}
          <div className="absolute inset-0 z-0" aria-hidden>
            <img
              src={`${import.meta.env.BASE_URL}images/auth-bg.jpg`}
              alt="Illustration financière"
              className="w-full h-full object-cover scale-105"
              loading="lazy"
              onError={(e) => {
                // Fallback si l'image locale n'est pas trouvée
                (e.currentTarget as HTMLImageElement).src =
                  "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?q=80&w=1600&auto=format&fit=crop";
              }}
            />
            <div className="absolute inset-0 bg-gradient-to-br from-background/10 via-background/20 to-background/30" />
          </div>
          <div className="relative z-10 max-w-md space-y-6 animate-in fade-in slide-in-from-left-4 duration-500">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-primary rounded-lg flex items-center justify-center">
                <TrendingUp className="w-7 h-7 text-primary-foreground" />
              </div>
              <h1 className="text-3xl font-bold text-foreground">CasaTrader</h1>
            </div>
            <p className="text-muted-foreground">
              Accédez à des outils professionnels pour suivre le marché, découvrir les opportunités et rester informé.
            </p>
            <ul className="text-sm text-muted-foreground space-y-2">
              <li>• Widgets TradingView intégrés</li>
              <li>• Expérience fluide et responsive</li>
              <li>• Sécurité renforcée</li>
            </ul>
          </div>
        </div>

        {/* Formulaire */}
        <div className="flex items-center justify-center p-6 md:p-10">
          <div className="w-full max-w-md animate-in fade-in slide-in-from-bottom-2 duration-300">
            <Card className="shadow-sm">
              <CardHeader className="space-y-1">
                <CardTitle className="text-2xl font-bold">
                  {isLogin ? "Connexion" : "Créer un compte"}
                </CardTitle>
                <CardDescription>
                  {isLogin ? "Ravi de vous revoir" : "Inscrivez-vous pour démarrer"}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Form {...form}>
                  <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4" noValidate>
                    <FormField
                      control={form.control}
                      name="email"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Email</FormLabel>
                          <FormControl>
                            <div className="relative">
                              <Mail className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                              <Input type="email" placeholder="votre@email.com" className="pl-9" autoComplete="email" {...field} />
                            </div>
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name="password"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Mot de passe</FormLabel>
                          <FormControl>
                            <div className="relative">
                              <Lock className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                              <Input
                                type={showPassword ? "text" : "password"}
                                placeholder="••••••••"
                                className="pl-9 pr-10"
                                autoComplete={isLogin ? "current-password" : "new-password"}
                                {...field}
                              />
                              <button
                                type="button"
                                aria-label={showPassword ? "Masquer le mot de passe" : "Afficher le mot de passe"}
                                onClick={() => setShowPassword((s) => !s)}
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                              >
                                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                              </button>
                            </div>
                          </FormControl>
                          <div className="flex items-center justify-between text-sm mt-1">
                            <span />
                            {isLogin && (
                              <button type="button" onClick={handleResetPassword} className="text-primary hover:underline">
                                Mot de passe oublié ?
                              </button>
                            )}
                          </div>
                          <FormMessage />
                        </FormItem>
                      )}
                    />

                    <Button type="submit" className="w-full bg-gradient-primary" disabled={loading || !form.formState.isValid}>
                      {loading ? "Chargement…" : isLogin ? "Se connecter" : "S'inscrire"}
                    </Button>
                  </form>
                </Form>

                <div className="mt-3 flex items-center justify-between text-sm">
                  <button type="button" onClick={() => setIsLogin(!isLogin)} className="text-primary hover:underline">
                    {isLogin ? "Pas encore de compte ?" : "Déjà un compte ?"}
                  </button>
                </div>

                <div className="mt-6">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="flex-1 h-px bg-border" />
                    <span className="text-xs text-muted-foreground">ou</span>
                    <div className="flex-1 h-px bg-border" />
                  </div>
                  <div className="grid grid-cols-1 gap-2">
                    <Button type="button" variant="outline" disabled={loading} onClick={() => handleOAuth("google")}>
                      <GoogleIcon className="w-4 h-4 mr-2" />
                      Continuer avec Google
                    </Button>
                    <Button type="button" variant="outline" disabled={loading} onClick={() => handleOAuth("facebook")}>
                      <Facebook className="w-4 h-4 mr-2 text-[#1877F2]" />
                      Continuer avec Facebook
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

// Google brand icon (SVG)
function GoogleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 533.5 544.3" xmlns="http://www.w3.org/2000/svg">
      <path d="M533.5 278.4c0-17.4-1.6-34.1-4.7-50.2H272v95.1h147c-6.3 33.9-25 62.7-53.3 82v68.1h85.9c50.2-46.3 81.9-114.5 81.9-195z" fill="#4285f4" />
      <path d="M272 544.3c72.6 0 133.6-24.1 178.1-65.9l-85.9-68.1c-23.8 16-54.2 25.5-92.2 25.5-70.7 0-130.7-47.7-152.2-111.9H31.6v70.2c44.1 87.5 134.5 150.2 240.4 150.2z" fill="#34a853" />
      <path d="M119.8 323.9c-10.2-30.6-10.2-64 0-94.6V159H31.6c-41.9 83.8-41.9 182.5 0 266.3l88.2-101.4z" fill="#fbbc04" />
      <path d="M272 106.1c39.5-.6 77.5 13.8 106.7 40.8l80-80C412.4 23.4 346.3-.4 272 0 166.1 0 75.7 62.7 31.6 150.2l88.2 70.1C141.3 153.3 201.3 106.1 272 106.1z" fill="#ea4335" />
    </svg>
  );
}
