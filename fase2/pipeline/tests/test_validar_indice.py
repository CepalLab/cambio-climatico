import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "validar_indice.py"
spec = importlib.util.spec_from_file_location("validar_indice", path)
validar_indice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validar_indice)

class RegresionIndiceTest(unittest.TestCase):
    def validar(self, titulos, esperadas=None, jerarquia=None):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            doc = {"documento": {"tiene_resumen_ejecutivo": True}, "resumen_secciones": [{"seccion": t, "nivel": 1, "subsecciones": []} for t in titulos]}
            esperadas = esperadas or ["I. T\u00edtulo literal", "II. Segundo t\u00edtulo"]
            jerarquia = jerarquia or [{"titulo": titulo, "nivel": 1} for titulo in esperadas]
            indice = {"fuente_inspeccionada": "tramos", "has_executive_summary": True, "secciones_nivel_1_incluidas": esperadas, "secciones_jerarquicas_incluidas": jerarquia, "titulos_excluidos": ["Resumen Ejecutivo"]}
            ruta_doc, ruta_indice = raiz / "documento.json", raiz / "indice_fuente.json"
            ruta_doc.write_text(json.dumps(doc), encoding="utf-8")
            ruta_indice.write_text(json.dumps(indice), encoding="utf-8")
            return validar_indice.validar(ruta_doc, ruta_indice)

    def test_rechaza_resumen_ejecutivo_incluido(self):
        self.assertTrue(any("excluida" in e for e in self.validar(["Resumen Ejecutivo", "I. Título literal", "II. Segundo título"])))

    def test_rechaza_foreword_incluido(self):
        self.assertTrue(any("excluida" in e for e in self.validar(["Foreword", "I. T?tulo literal", "II. Segundo t?tulo"])))

    def test_rechaza_titulo_reformulado(self):
        self.assertTrue(any("títulos, orden o cobertura" in e for e in self.validar(["I. Título reformulado", "II. Segundo título"])))

    def test_rechaza_seccion_omitida(self):
        self.assertTrue(any("títulos, orden o cobertura" in e for e in self.validar(["I. Título literal"])))

    def test_acepta_caso_correcto(self):
        self.assertEqual([], self.validar(["I. Título literal", "II. Segundo título"]))

    def test_acepta_resumen_de_recomendaciones_final(self):
        titulos = ["I. Diagnostico", "III. Resumen de recomendaciones"]
        self.assertEqual([], self.validar(titulos, titulos))


    def test_rechaza_subtitulo_recortado(self):
        jerarquia = [{"titulo": "I. T\u00edtulo literal", "nivel": 1}, {"titulo": "A. Subt\u00edtulo literal completo", "nivel": 2}, {"titulo": "II. Segundo t\u00edtulo", "nivel": 1}]
        errores = self.validar(["I. T\u00edtulo literal", "A. Subt\u00edtulo recortado", "II. Segundo t\u00edtulo"], ["I. T\u00edtulo literal", "II. Segundo t\u00edtulo"], jerarquia)
        self.assertTrue(any("cobertura de la jerarqu" in error for error in errores))

    def test_rechaza_subtitulos_fuera_de_orden(self):
        jerarquia = [{"titulo": "I. T\u00edtulo literal", "nivel": 1}, {"titulo": "A. Primero", "nivel": 2}, {"titulo": "B. Segundo", "nivel": 2}, {"titulo": "II. Segundo t\u00edtulo", "nivel": 1}]
        errores = self.validar(["I. T\u00edtulo literal", "B. Segundo", "A. Primero", "II. Segundo t\u00edtulo"], ["I. T\u00edtulo literal", "II. Segundo t\u00edtulo"], jerarquia)
        self.assertTrue(any("cobertura de la jerarqu" in error for error in errores))
if __name__ == "__main__":
    unittest.main()
