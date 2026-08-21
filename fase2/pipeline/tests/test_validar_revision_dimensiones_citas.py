import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "validar_revision_dimensiones_citas.py"
spec = importlib.util.spec_from_file_location("validar_revision", path)
validar_revision = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validar_revision)


class ReviewMatrixTest(unittest.TestCase):
    def validate(self, payload):
        with tempfile.TemporaryDirectory() as directory:
            matrix = Path(directory) / "matrix.json"
            matrix.write_text(json.dumps(payload), encoding="utf-8")
            return validar_revision.validate(matrix)

    def test_accepts_direct_entry(self):
        payload = {"entradas": [{"ruta_seccion": "/I", "dimension": "desafios", "pagina": 2, "veredicto": "directa", "justificacion": "La cita prueba el riesgo."}]}
        self.assertEqual([], self.validate(payload))

    def test_rejects_unsupported_entry(self):
        payload = {"entradas": [{"ruta_seccion": "/I", "dimension": "desafios", "pagina": 2, "veredicto": "no_sustenta", "justificacion": "La cita es tangencial."}]}
        self.assertTrue(self.validate(payload))

    def test_partial_requires_human_decision(self):
        payload = {"entradas": [{"ruta_seccion": "/I", "dimension": "desafios", "pagina": 2, "veredicto": "parcial", "justificacion": "Soporte incompleto."}]}
        self.assertTrue(self.validate(payload))


if __name__ == "__main__":
    unittest.main()
