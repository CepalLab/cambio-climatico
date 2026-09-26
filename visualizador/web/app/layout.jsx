import "./globals.css";

export const metadata = {
  title: "El clima en la CEPAL — Explorador del corpus 2015–2026",
  description:
    "238 publicaciones de la CEPAL sobre cambio climático, enriquecidas y navegables por división, tema, tipología e interpelación.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>
        <header className="barra">
          <nav>
            <a className="marca" href="/">Clima · CEPAL</a>
            <a href="/#divisiones">Divisiones</a>
            <a href="/#temas">Temas</a>
            <a href="/#destacados">Destacados</a>
            <a href="/#costos">Costos</a>
            <a href="/#metodologia">Método</a>
          </nav>
        </header>
        {children}
        <footer className="pie">
          <div className="contenedor">
            <p>
              Explorador del corpus CEPAL sobre cambio climático (2015–2026).
              Documentos: <a href="https://repositorio.cepal.org">repositorio.cepal.org</a>.
            </p>
            <p>
              Diseño inspirado en{" "}
              <a href="https://www.1kpapers.com/">1kpapers.com</a> de{" "}
              <a href="https://github.com/Nutlope/1kpapers">Nutlope</a> (MIT),
              con todos los créditos inspiracionales: fuentes, tarjetas,
              carrusel, línea de tiempo, benchmark de costos y relato
              metodológico. Aquí las citas externas se sustituyen por
              evidencia interna (citas literales y dimensiones codificadas).
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
