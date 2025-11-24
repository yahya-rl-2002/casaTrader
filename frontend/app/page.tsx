import Link from "next/link";

export default function HomePage() {
  return (
    <section className="flex flex-col items-center justify-center py-24 gap-6">
      <h1 className="text-4xl font-bold text-center">
        Casablanca Fear &amp; Greed Index
      </h1>
      <p className="max-w-2xl text-center text-slate-300">
        Visualisez le sentiment des investisseurs marocains via un indice quotidien basé sur le marché, les obligations et l&apos;analyse média.
      </p>
      <Link
        href="/dashboard"
        className="inline-flex items-center justify-center rounded-md bg-greed-500 px-6 py-3 font-semibold text-slate-900 transition hover:bg-greed-700"
      >
        Accéder au dashboard
      </Link>
    </section>
  );
}



