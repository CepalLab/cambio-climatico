import { agg, docs } from "../../../lib/datos";
import DocCard from "../../../components/DocCard";

export function generateStaticParams() {
  return agg.divisiones.map((d) => ({ slug: d.slug }));
}

export default function Division({ params }) {
  const div = agg.divisiones.find((d) => d.slug === params.slug);
  if (!div) return <main className="contenedor"><p>División no encontrada.</p></main>;
  const lista = docs.filter((d) => d.division === div.nombre);
  return (
    <main className="contenedor" style={{ padding: "32px 20px 56px" }}>
      <a href="/">← Volver al explorador</a>
      <h1>{div.nombre}</h1>
      <p className="doc-meta">{lista.length} documentos</p>
      <div className="rejilla" style={{ marginTop: 16 }}>
        {lista.map((d) => (
          <DocCard key={d.id} doc={d} />
        ))}
      </div>
    </main>
  );
}
