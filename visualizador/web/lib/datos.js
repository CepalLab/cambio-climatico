import agregados from "../data/agregados.json";
import documentos from "../data/documentos.json";

export const docs = documentos;
export const agg = agregados;
export const porId = Object.fromEntries(documentos.map((d) => [d.id, d]));

export function tituloCorto(t, n = 90) {
  if (!t) return "";
  return t.length > n ? t.slice(0, n - 1) + "…" : t;
}
