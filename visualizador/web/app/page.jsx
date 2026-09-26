import { agg, docs, porId } from "../lib/datos";
import DocCard from "../components/DocCard";

const T = agg.totales;

function Seccion({ id, num, titulo, bajada, children }) {
  return (
    <section className="bloque" id={id}>
      <div className="contenedor">
        <div className="numero-seccion">{num}</div>
        <h2>{titulo}</h2>
        {bajada && <p className="bajada">{bajada}</p>}
        {children}
      </div>
    </section>
  );
}

export default function Home() {
  const maxDiv = Math.max(...agg.divisiones.map((d) => d.total));
  const maxTema = Math.max(...agg.temas.map((d) => d.total));
  const destacados = agg.destacados.map((id) => porId[id]).filter(Boolean);
  const brechas = agg.dimensiones.find((d) => d.dimension === "brechas_implementacion");
  const avances = agg.dimensiones.find((d) => d.dimension === "avances_implementacion");

  return (
    <main>
      <div className="hero">
        <div className="contenedor">
          <div className="kicker">CEPAL Lab · 2015–2026</div>
          <h1>El clima en la CEPAL</h1>
          <p>
            {T.documentos} publicaciones que mapean la investigación climática
            de la CEPAL entre {T.periodo[0]} y {T.periodo[1]}, con{" "}
            {T.dimensiones.toLocaleString("es")} fragmentos codificados y{" "}
            {T.citas.toLocaleString("es")} citas literales.
          </p>
        </div>
      </div>

      <Seccion
        id="divisiones"
        num="01 · Divisiones"
        titulo="Explorar por división"
        bajada="El equivalente a los laboratorios del sitio de referencia: cada división de la CEPAL con su producción climática."
      >
        <div className="rejilla">
          {agg.divisiones.map((d) => (
            <a className="tarjeta" key={d.slug} href={`/division/${d.slug}/`}>
              <div className="total">{d.total}</div>
              <div className="nombre">{d.nombre}</div>
              <div className="barra-h">
                <span style={{ width: `${(100 * d.total) / maxDiv}%` }} />
              </div>
            </a>
          ))}
        </div>
      </Seccion>

      <Seccion
        id="temas"
        num="02 · Temas"
        titulo="Explorar por tema"
        bajada="Vocabulario controlado cepal.topicSpa. Cambio climático es el agregador de todo el corpus (como AI en el referente), así que aquí van los demás temas."
      >
        <ol className="lista-temas">
          {agg.temas.slice(0, 24).map((t, i) => (
            <li key={t.slug}>
              <a href={`/tema/${t.slug}/`}>
                <span className="pos">{String(i + 1).padStart(2, "0")}</span>
                {t.nombre}
                <span className="n">{t.total}</span>
              </a>
            </li>
          ))}
        </ol>
      </Seccion>

      <Seccion
        id="destacados"
        num="03 · Destacados"
        titulo="Los documentos con más evidencia"
        bajada="Sin citas externas, ordenamos por evidencia interna: dimensiones codificadas más citas literales verificadas en página. Es cobertura, no un ranking de calidad."
      >
        <div className="carrusel">
          {destacados.map((d) => (
            <DocCard key={d.id} doc={d} />
          ))}
        </div>
      </Seccion>

      <Seccion
        id="tipologia"
        num="04 · Transformaciones"
        titulo="¿Qué transformación impulsa cada documento?"
        bajada="Tipología propia calibrada con el equipo del curso, sobre el canon de las 11 Grandes Transformaciones."
      >
        <div className="rejilla">
          {agg.tipologia.map((t) => (
            <div className="tarjeta" key={t.nombre}>
              <div className="total">{t.total}</div>
              <div className="nombre">{t.nombre}</div>
            </div>
          ))}
        </div>
      </Seccion>

      <Seccion
        id="interpelacion"
        num="05 · Interpelación"
        titulo="¿Qué le exige cada documento a la política?"
        bajada="Cuatro criterios con veredicto Sí, Parcial o No y evidencia literal. El gran impulso ambiental es el más exigente: solo 63 documentos lo cumplen del todo."
      >
        <div className="rejilla">
          {agg.interpelacion.map((c) => (
            <div className="tarjeta" key={c.criterio}>
              <div className="nombre">{c.nombre}</div>
              <p className="doc-meta">
                <span className="pildora si">Sí · {c.si}</span>
                <span className="pildora parcial">Parcial · {c.parcial}</span>
                <span className="pildora no">No · {c.no}</span>
              </p>
            </div>
          ))}
        </div>
      </Seccion>

      <Seccion
        id="brechas"
        num="06 · Brechas"
        titulo="Avances frente a brechas de implementación"
        bajada={`Lo reportado como avance (${avances?.total ?? "—"} fragmentos) frente a lo señalado como brecha (${brechas?.total ?? "—"}). Las dimensiones completas están en cada ficha.`}
      >
        <div className="rejilla">
          {agg.dimensiones.map((d) => (
            <div className="tarjeta" key={d.dimension}>
              <div className="total">{d.total}</div>
              <div className="nombre">{d.nombre}</div>
              <div className="barra-h">
                <span
                  style={{
                    width: `${(100 * d.total) / agg.dimensiones[0].total}%`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </Seccion>

      <Seccion
        id="timeline"
        num="07 · Tiempo"
        titulo="Explorar por año"
        bajada="Tres períodos de calendario: 2015–2018, 2019–2022 y 2023–2026."
      >
        <div className="timeline">
          {agg.timeline.map((t) => (
            <a key={t.anio} href={`#`}>
              <div className="a">{t.anio}</div>
              <div className="t">{t.total} docs</div>
            </a>
          ))}
        </div>
      </Seccion>

      <Seccion
        id="costos"
        num="08 · Costos"
        titulo="¿Cuánto costó enriquecer el corpus?"
        bajada="Sección en construcción: se completará con el usage reportado por los proveedores y la fecha de uso de cada lote. Metodología de costeo en el reporte metodológico interno."
      >
        <div className="rejilla">
          {["Gemini (enriquecimiento)", "Claude (calibración)", "Costo total"].map(
            (m) => (
              <div className="tarjeta" key={m}>
                <div className="total">—</div>
                <div className="nombre">{m}</div>
                <div className="doc-meta">pendiente de datos</div>
              </div>
            )
          )}
        </div>
      </Seccion>

      <Seccion
        id="metodologia"
        num="09 · Método"
        titulo="Cómo convertimos 238 PDFs en un atlas navegable"
        bajada="Versión simplificada. El relato completo vive en el reporte metodológico interno del proyecto."
      >
        <ol className="pasos">
          <li>
            <strong>Congelar un corpus reproducible.</strong> Filtro por tema
            cambio climático, exclusión de duplicados y administrativos, 14
            documentos estratégicos agregados: 244 → 238.
          </li>
          <li>
            <strong>Calibrar con expertos.</strong> Codebook, tipología e
            interpelación probados en 17 documentos con revisor ciego
            (66% → 85% de acuerdo) y confirmación del equipo del curso.
          </li>
          <li>
            <strong>Leer cada PDF.</strong> Extracción de texto, índice
            jerárquico y enriquecimiento por secciones con citas literales y
            página declarada.
          </li>
          <li>
            <strong>Validar todo.</strong> Cuatro validadores (esquema, índice,
            citas, densidad), certificados gemelos y revisión humana por lote
            antes de promover cada documento.
          </li>
          <li>
            <strong>Sintetizar y navegar.</strong> Informe maestro, figuras
            reproducibles y este explorador por división, tema, tipología e
            interpelación.
          </li>
        </ol>
      </Seccion>
    </main>
  );
}
