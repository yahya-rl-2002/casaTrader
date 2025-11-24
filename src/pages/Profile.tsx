import { useEffect, useMemo, useState } from "react";
import { useSession } from "@/hooks/use-session";
import { supabase } from "@/integrations/supabase/client";
import { useTheme } from "next-themes";
import { Link } from "react-router-dom";
import { Navigation } from "@/components/Navigation";
import { Footer } from "@/components/Footer";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog";
import { toast } from "@/components/ui/sonner";
import { cn } from "@/lib/utils";

export default function Profile() {
  const { user } = useSession();
  const { setTheme, theme } = useTheme();

  const initials = useMemo(() => {
    const email = user?.email ?? "";
    const local = (email.split("@")[0] ?? "").replace(/[^A-Za-z0-9]/g, "");
    const up = local.toUpperCase();
    if (up.length >= 2) return up.slice(0, 2);
    if (up.length === 1) return up + "_";
    return "US";
  }, [user?.email]);

  // Personal info
  const [fullName, setFullName] = useState<string>("");
  const [phone, setPhone] = useState<string>("");
  const [avatarUploading, setAvatarUploading] = useState(false);
  const email = user?.email ?? "";
  const [editingInfo, setEditingInfo] = useState(false);

  // Security
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [mfaEnabled, setMfaEnabled] = useState(false);

  // Personalization
  const [lang, setLang] = useState<string>("fr");

  // Subscription
  const plan = (user?.user_metadata?.plan as string) || "Gratuit";
  const planExpiry = (user?.user_metadata?.plan_expiry as string) || null;

  const lastLogin = (user as any)?.last_sign_in_at as string | undefined;

  useEffect(() => {
    setFullName((user?.user_metadata?.full_name as string) || "");
    setPhone((user?.user_metadata?.phone as string) || "");
    setLang(((user?.user_metadata?.lang as string) || localStorage.getItem("lang") || "fr") as string);
    setMfaEnabled(Boolean(user?.user_metadata?.mfa_enabled));
  }, [user]);

  async function savePersonalInfo() {
    try {
      const { error } = await supabase.auth.updateUser({ data: { full_name: fullName, phone, lang, mfa_enabled: mfaEnabled } });
      if (error) throw error;
      toast("Informations mises à jour");
      setEditingInfo(false);
    } catch (e) {
      toast("Erreur lors de la mise à jour");
    }
  }

  async function onAvatarChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file || !user) return;
    setAvatarUploading(true);
    try {
      const ext = file.name.split(".").pop() || "png";
      const path = `${user.id}.${ext}`;
      const { error: upErr } = await supabase.storage.from("avatars").upload(path, file, { upsert: true, cacheControl: "3600" });
      if (upErr) throw upErr;
      const { data: pub } = supabase.storage.from("avatars").getPublicUrl(path);
      const url = pub?.publicUrl;
      const { error } = await supabase.auth.updateUser({ data: { avatar_url: url } });
      if (error) throw error;
      toast("Photo de profil mise à jour");
    } catch (e) {
      toast("Échec du téléversement (configurer le bucket 'avatars')");
    } finally {
      setAvatarUploading(false);
      e.currentTarget.value = "";
    }
  }

  async function changePassword() {
    if (!newPassword || newPassword !== confirmPassword) {
      toast("Les mots de passe ne correspondent pas");
      return;
    }
    try {
      const { error } = await supabase.auth.updateUser({ password: newPassword });
      if (error) throw error;
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      toast("Mot de passe mis à jour");
    } catch (e) {
      toast("Impossible de changer le mot de passe");
    }
  }

  function updateLang(value: string) {
    setLang(value);
    try { localStorage.setItem("lang", value); } catch {}
  }

  async function toggleMfa(next: boolean) {
    setMfaEnabled(next);
    try { await supabase.auth.updateUser({ data: { mfa_enabled: next } }); } catch {}
  }

  async function deleteAccount() {
    try {
      const { error } = await supabase.functions.invoke("delete-user", { body: {} });
      if (error) throw error;
      toast("Compte supprimé");
    } catch (e) {
      toast("Suppression non disponible côté client. Contactez le support.");
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Profil utilisateur</h1>
          <p className="text-muted-foreground">Gérez vos informations, sécurité et préférences.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left column: personal + security */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Informations personnelles</CardTitle>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="flex items-center gap-4">
                  <Avatar className="h-16 w-16">
                    <AvatarFallback className="bg-primary/10 text-primary font-semibold">{initials}</AvatarFallback>
                  </Avatar>
                  <div>
                    <Label htmlFor="avatar" className={cn("inline-flex items-center gap-2 text-sm", avatarUploading && "opacity-70")}>Photo de profil</Label>
                    <div>
                      <Input id="avatar" type="file" accept="image/*" disabled={avatarUploading} onChange={onAvatarChange} className="max-w-xs mt-1 cursor-pointer" />
                    </div>
                  </div>
                </div>

                <Separator />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="fullName">Nom complet</Label>
                    <Input id="fullName" value={fullName} disabled={!editingInfo} onChange={(e) => setFullName(e.target.value)} placeholder="Votre nom" />
                  </div>
                  <div>
                    <Label htmlFor="email">Adresse email</Label>
                    <Input id="email" value={email} disabled readOnly />
                  </div>
                  <div>
                    <Label htmlFor="phone">Téléphone (facultatif)</Label>
                    <Input id="phone" value={phone} disabled={!editingInfo} onChange={(e) => setPhone(e.target.value)} placeholder="Ex: +212…" />
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {!editingInfo ? (
                    <Button onClick={() => setEditingInfo(true)}>Modifier les informations</Button>
                  ) : (
                    <>
                      <Button className="bg-gradient-primary" onClick={savePersonalInfo}>Enregistrer</Button>
                      <Button variant="outline" onClick={() => setEditingInfo(false)}>Annuler</Button>
                    </>
                  )}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Paramètres de sécurité</CardTitle>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="md:col-span-1">
                    <Label htmlFor="currentPassword">Mot de passe actuel</Label>
                    <Input id="currentPassword" type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} placeholder="••••••••" />
                  </div>
                  <div>
                    <Label htmlFor="newPassword">Nouveau mot de passe</Label>
                    <Input id="newPassword" type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} />
                  </div>
                  <div>
                    <Label htmlFor="confirmPassword">Confirmer</Label>
                    <Input id="confirmPassword" type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
                  </div>
                </div>
                <div>
                  <Button onClick={changePassword}>Changer le mot de passe</Button>
                </div>
                <Separator />
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium">Vérification en deux étapes (2FA)</div>
                    <div className="text-sm text-muted-foreground">Sécurisez davantage votre compte (stocké dans vos métadonnées).</div>
                  </div>
                  <Switch checked={mfaEnabled} onCheckedChange={toggleMfa} />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right column: preferences + subscription + activity + danger */}
          <div className="space-y-6">
            <Card id="settings">
              <CardHeader>
                <CardTitle>Personnalisation</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 gap-4">
                  <div>
                    <Label>Thème</Label>
                    <div className="mt-2 flex gap-2">
                      <Button variant={theme === "light" ? "default" : "outline"} onClick={() => setTheme("light")}>Clair</Button>
                      <Button variant={theme === "dark" ? "default" : "outline"} onClick={() => setTheme("dark")}>Sombre</Button>
                    </div>
                  </div>
                  <div>
                    <Label>Langue</Label>
                    <div className="mt-2 w-48">
                      <Select value={lang} onValueChange={updateLang}>
                        <SelectTrigger>
                          <SelectValue placeholder="Choisir une langue" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="fr">Français</SelectItem>
                          <SelectItem value="en">English</SelectItem>
                          <SelectItem value="es">Español</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Abonnement</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-muted-foreground">Plan actuel</div>
                  <div className="font-medium">{plan}</div>
                </div>
                <div className="flex items-center justify-between">
                  <div className="text-sm text-muted-foreground">Expiration</div>
                  <div className="font-medium">{planExpiry ? new Date(planExpiry).toLocaleDateString() : "—"}</div>
                </div>
                <div className="mt-3">
                  <Link to="/pricing">
                    <Button className="bg-gradient-primary w-full">Mettre à niveau</Button>
                  </Link>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Historique et activité</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-muted-foreground">Dernière connexion</div>
                  <div className="font-medium">{lastLogin ? new Date(lastLogin).toLocaleString() : "—"}</div>
                </div>
                <Link to="/activity">
                  <Button variant="outline" className="w-full">Voir l'historique des activités</Button>
                </Link>
              </CardContent>
            </Card>

            <Card className="border-destructive/30">
              <CardHeader>
                <CardTitle className="text-destructive">Suppression de compte</CardTitle>
              </CardHeader>
              <CardContent>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button variant="destructive" className="w-full">Supprimer mon compte</Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>Suppression définitive</AlertDialogTitle>
                      <AlertDialogDescription>
                        Cette action est irréversible. Toutes vos données seront supprimées. Confirmez-vous la suppression de votre compte ?
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Annuler</AlertDialogCancel>
                      <AlertDialogAction onClick={deleteAccount}>Supprimer</AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

