import { docs, porId } from "../../../lib/datos";
import { Portada } from "../../../components/DocCard";

export function generateStaticParams() {
  return docs.map((d) => ({ id: d.id }));
}

const NOMBRES = {
  gran_impulso_ambiental_concreto: "Gran impulso ambiental",
  articulacion_actores: "Articulación de actores",
  oportunidades_productivas_sostenibles: "Oportunidades productivas",
  como_hacerlo_concreto: "Cómo hacerlo concreto",
};

export default function Documento({ params }) {
  const doc = porId[params.id];
  if (!doc) return <main className="contenedor"><p>Documento no encontrado.</p></main>;
  return (
    <main className="contenedor" style={{ padding: "32px 20px 56px" }}>
      <a href="/">← Volver al explorador</a>
      <div className="ficha" style={{ marginTop: 16 }}>
        <div style={{ display: "grid", gridTemplateColumns: "220px 1fr", gap: 24 }}>
          <Portada doc={doc} />
          <div>
            <h1 style={{ fontSize: 28 }}>{doc.titulo}</h1>
            <p className="doc-meta">
              {doc.anio} · {doc.division} · {doc.tipo}
            </p>
            <p>
              <span className="pildora neutra">{doc.secciones} secciones</span>
              <span className="pildora neutra">{doc.dimensiones} dimensiones</span>
              <span className="pildora neutra">{doc.citas} citas literales</span>
            </p>
            <p>
              <a href={doc.handle}>Ver en repositorio.cepal.org →</a>
            </p>
          </div>
        </div>
        {doc.resumen && (
          <>
            <h3>Resumen</h3>
            <p>{doc.resumen}</p>
          </>
        )}
        <h3>Temas</h3>
        <p>
          {doc.temas.map((t) => (
            <span className="pildora neutra" key={t}>{t}</span>
          ))}
        </p>
        {doc.tipologia && (
          <>
            <h3>Tipología</h3>
            <p>
              Primaria: <strong>{doc.tipologia.primaria}</strong>
              {doc.tipologia.secundaria && (
                <> · Secundaria: <strong>{doc.tipologia.secundaria}</strong></>
              )}
            </p>
          </>
        )}
        <h3>Interpelación</h3>
        {Object.entries(NOMBRES).map(([crit, nombre]) => {
          const r = doc.interpelacion[crit];
          if (!r) return null;
          const v = (r.veredicto || "").toLowerCase();
          return (
            <div key={crit}>
              <p>
                <strong>{nombre}:</strong>{" "}
                <span className={`pildora ${v}`}>{r.veredicto}</span>
              </p>
              {r.evidencia && <div className="cita">{r.evidencia}</div>}
            </div>
          );
        })}
      </div>
    </main>
  );
}
