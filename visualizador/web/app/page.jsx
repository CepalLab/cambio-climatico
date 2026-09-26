import { agg, docs, porId } from "../lib/datos";
import Carrusel from "../components/Carrusel";

const T = agg.totales;
const COLORES = ["#1f4fd8", "#cf3a26", "#2e7d4b", "#8a5a00", "#6a3ec0", "#0e7c86"];

function iniciales(nombre) {
  return nombre
    .split(" ")
    .filter((w) => w.length > 2)
    .slice(0, 2)
    .map((w) => w[0])
    .join("")
    .toUpperCase();
}

function Seccion({ num, titulo, bajada, children }) {
  return (
    <section className="bloque">
      <div className="contenedor">
        <div className="etiqueta">{num}</div>
        <h2>{titulo}</h2>
        {bajada && <p className="bajada">{bajada}</p>}
        {children}
      </div>
    </section>
  );
}

export default function Home() {
  const destacados = agg.destacados.map((id) => porId[id]).filter(Boolean);
  const topEvidencia = [...docs].sort((a, b) => b.evidencia - a.evidencia).slice(0, 3);
  const elegido = destacados[(new Date().getDate() + new Date().getMonth()) % destacados.length];
  const brechas = agg.dimensiones.find((d) => d.dimension === "brechas_implementacion");
  const avances = agg.dimensiones.find((d) => d.dimension === "avances_implementacion");

  return (
    <main>
      <div className="hero">
        <div className="contenedor">
          <h1>El clima en la CEPAL</h1>
          <p>
            {T.documentos} documentos que mapean la investigación climática de
            la CEPAL entre {T.periodo[0]} y {T.periodo[1]}.
          </p>

          <div className="tira-labs" id="divisiones">
            <div className="celda">
              <div className="etiqueta">Explorar por división</div>
            </div>
            {agg.divisiones.slice(0, 6).map((d, i) => (
              <a className="celda" key={d.slug} href={`/division/${d.slug}/`}>
                <span
                  className="insignia"
                  style={{ background: COLORES[i % COLORES.length] }}
                >
                  {iniciales(d.nombre)}
                </span>
                {d.nombre.length > 26 ? d.nombre.slice(0, 25) + "…" : d.nombre}
              </a>
            ))}
          </div>

          <div className="grilla-main">
            <div id="temas">
              <div className="etiqueta">Explorar por temas</div>
              <ol className="lista-temas">
                {agg.temas.slice(0, 6).map((t, i) => (
                  <li key={t.slug}>
                    <a href={`/tema/${t.slug}/`}>
                      <span className="pos">{String(i + 1).padStart(2, "0")}</span>
                      {t.nombre}
                      <span className="n">{t.total}</span>
                    </a>
                  </li>
                ))}
              </ol>
              <p>
                <a className="ver-todo" href="#temas-todos">Ver todos los temas →</a>
              </p>
            </div>

            <div className="trending" id="destacados">
              <div className="etiqueta" style={{ color: "var(--rojo)" }}>
                01 · Tendencia del corpus
              </div>
              <h2>Los documentos que movieron la agenda climática</h2>
              <p className="bajada">
                Seleccionados por evidencia interna: dimensiones codificadas
                y citas literales verificadas en página.
              </p>
              <Carrusel docs={destacados} />
            </div>

            <div id="evidencia">
              <div className="etiqueta" style={{ textAlign: "right", display: "block" }}>
                Más evidencia
              </div>
              <ol className="ranking">
                {topEvidencia.map((d, i) => (
                  <li key={d.id}>
                    <span className="pos">{String(i + 1).padStart(2, "0")}</span>
                    <a href={`/documento/${d.id}/`}>
                      {d.titulo}
                      <span className="fecha"> · {d.anio}</span>
                    </a>
                    <span className="cifra">{d.evidencia}</span>
                  </li>
                ))}
              </ol>
            </div>
          </div>

          <div className="timeline-strip">
            <div>
              <div className="etiqueta" style={{ padding: "16px 20px 0" }}>
                Explorar por año
              </div>
              <div className="anios">
                {agg.timeline.map((t) => (
                  <a key={t.anio} href={`/anio/${t.anio}/`}>
                    <div className="a">{t.anio}</div>
                    <div className="punto" />
                    <div className="t">{t.total}</div>
                  </a>
                ))}
              </div>
            </div>
            <div className="total">
              <span className="cifra">{T.documentos}</span>
              <span className="txt">documentos<br />curados e indexados</span>
            </div>
          </div>

          {elegido && (
            <div className="elegido">
              <div>
                <div className="marca-e">✦</div>
                <div className="etiqueta" style={{ marginTop: 12 }}>
                  Este documento
                  <br />
                  fue elegido
                  <br />
                  para ti
                </div>
              </div>
              <div>
                <div className="etiqueta">
                  {elegido.division} / {elegido.anio}
                </div>
                <h3>{elegido.titulo}</h3>
                <p>{(elegido.resumen || "").slice(0, 280)}…</p>
              </div>
              <div>
                <a className="ver-todo" href={`/documento/${elegido.id}/`}>
                  LEER EL DOCUMENTO →
                </a>
              </div>
            </div>
          )}
        </div>
      </div>

      <Seccion
        num="El benchmark de costos"
        titulo={`¿Cuánto costó enriquecer ${T.documentos} documentos?`}
        bajada="Sección en construcción: se completará con el usage reportado por los proveedores y la fecha de uso de cada lote. Es una comparación de costos, no un ranking de calidad."
      >
        <table className="costotabla" id="costos">
          <thead>
            <tr>
              <th></th>
              <th>MODELO</th>
              <th>INFERENCIA TOTAL</th>
              <th>POR DOCUMENTO</th>
              <th>RELATIVO</th>
            </tr>
          </thead>
          <tbody>
            {[
              ["01", "Gemini (enriquecimiento)"],
              ["02", "Claude (calibración)"],
            ].map(([n, m]) => (
              <tr key={m}>
                <td style={{ color: "var(--rojo)", fontFamily: "var(--mono)", fontSize: 12 }}>{n}</td>
                <td className="modelo">{m}</td>
                <td className="monto">—</td>
                <td className="monto">—</td>
                <td>pendiente de datos</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Seccion>

      <Seccion
        num="Temas · Tipología · Interpelación"
        titulo="El corpus por dentro"
        bajada="Tres formas de agrupar los mismos 238 documentos, todas derivadas del enriquecimiento calibrado."
      >
        <div id="temas-todos">
          <div className="etiqueta">Todos los temas ({agg.temas.length})</div>
          <ol className="lista-temas" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", display: "grid", gap: "0 16px" }}>
            {agg.temas.slice(0, 30).map((t, i) => (
              <li key={t.slug}>
                <a href={`/tema/${t.slug}/`}>
                  <span className="pos">{String(i + 1).padStart(2, "0")}</span>
                  {t.nombre}
                  <span className="n">{t.total}</span>
                </a>
              </li>
            ))}
          </ol>
        </div>
        <div className="etiqueta" style={{ marginTop: 24 }}>Transformaciones (tipología primaria)</div>
        <div className="rejilla" style={{ marginTop: 8 }}>
          {agg.tipologia.map((t) => (
            <div className="tarjeta" key={t.nombre}>
              <div className="total">{t.total}</div>
              <div className="nombre">{t.nombre}</div>
            </div>
          ))}
        </div>
        <div className="etiqueta" style={{ marginTop: 24 }}>Interpelación: veredictos por criterio</div>
        <div className="rejilla" style={{ marginTop: 8 }}>
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
        <div className="etiqueta" style={{ marginTop: 24 }}>
          Dimensiones · avances ({avances?.total}) frente a brechas ({brechas?.total})
        </div>
        <div className="rejilla" style={{ marginTop: 8 }}>
          {agg.dimensiones.map((d) => (
            <div className="tarjeta" key={d.dimension}>
              <div className="total">{d.total}</div>
              <div className="nombre">{d.nombre}</div>
              <div className="barra-h">
                <span style={{ width: `${(100 * d.total) / agg.dimensiones[0].total}%` }} />
              </div>
            </div>
          ))}
        </div>
      </Seccion>

      <Seccion
        num="Sobre el método"
        titulo="Cómo convertimos 238 PDFs en un atlas navegable"
        bajada="Versión simplificada. El relato completo vive en el reporte metodológico interno del proyecto."
      >
        <ol className="pasos" id="metodologia">
          <li><strong>Congelar un corpus reproducible.</strong> Filtro por tema cambio climático, exclusión de duplicados y administrativos, 14 documentos estratégicos agregados: 244 → 238.</li>
          <li><strong>Calibrar con expertos.</strong> Codebook, tipología e interpelación probados en 17 documentos con revisor ciego (66% → 85% de acuerdo).</li>
          <li><strong>Leer cada PDF.</strong> Extracción de texto, índice jerárquico y enriquecimiento por secciones con citas literales y página declarada.</li>
          <li><strong>Validar todo.</strong> Cuatro validadores (esquema, índice, citas, densidad), certificados gemelos y revisión humana por lote.</li>
          <li><strong>Sintetizar y navegar.</strong> Informe maestro, figuras reproducibles y este explorador.</li>
        </ol>
      </Seccion>
    </main>
  );
}
