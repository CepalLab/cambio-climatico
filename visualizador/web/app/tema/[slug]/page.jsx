import { agg, docs } from "../../../lib/datos";
import DocCard from "../../../components/DocCard";

export function generateStaticParams() {
  return agg.temas.map((t) => ({ slug: t.slug }));
}

export default function Tema({ params }) {
  const tema = agg.temas.find((t) => t.slug === params.slug);
  if (!tema) return <main className="contenedor"><p>Tema no encontrado.</p></main>;
  const lista = docs.filter((d) => d.temas.includes(tema.nombre));
  return (
    <main className="contenedor" style={{ padding: "32px 20px 56px" }}>
      <a href="/">← Volver al explorador</a>
      <h1>{tema.nombre}</h1>
      <p className="doc-meta">{lista.length} documentos</p>
      <div className="rejilla" style={{ marginTop: 16 }}>
        {lista.map((d) => (
          <DocCard key={d.id} doc={d} />
        ))}
      </div>
    </main>
  );
}
