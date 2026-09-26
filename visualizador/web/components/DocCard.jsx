import { tituloCorto } from "../lib/datos";

export function Portada({ doc, slug }) {
  if (doc.portada) {
    return (
      <img
        className="portada"
        src={`/portadas/${doc.id}.jpg`}
        alt={`Portada de ${doc.titulo}`}
        loading="lazy"
      />
    );
  }
  return (
    <div className="portada-fallback">
      <div className="anio">{doc.anio}</div>
      <div className="div">{doc.division}</div>
    </div>
  );
}

export default function DocCard({ doc }) {
  const href = `/documento/${doc.id}/`;
  return (
    <a className="tarjeta" href={href}>
      <Portada doc={doc} />
      <div className="doc-titulo">{tituloCorto(doc.titulo, 110)}</div>
      <div className="doc-meta">
        {doc.anio} · {doc.division} · {doc.evidencia} evidencias
      </div>
    </a>
  );
}
