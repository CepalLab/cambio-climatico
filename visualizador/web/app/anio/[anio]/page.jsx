import { agg, docs } from "../../../lib/datos";
import DocCard from "../../../components/DocCard";

export function generateStaticParams() {
  return agg.timeline.map((t) => ({ anio: String(t.anio) }));
}

export default function Anio({ params }) {
  const anio = Number(params.anio);
  const lista = docs.filter((d) => d.anio === anio);
  return (
    <main className="contenedor" style={{ padding: "32px 20px 56px" }}>
      <a href="/">← Volver al explorador</a>
      <h1>{anio}</h1>
      <p className="doc-meta">{lista.length} documentos</p>
      <div className="rejilla" style={{ marginTop: 16 }}>
        {lista.map((d) => (
          <DocCard key={d.id} doc={d} />
        ))}
      </div>
    </main>
  );
}
