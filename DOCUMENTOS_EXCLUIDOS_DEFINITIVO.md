# Documentos Excluidos - Lista Definitiva para Segunda Fase

**Fecha**: 2026-06-09  
**Estado**: Definitivo  
**Total excluidos**: 9 documentos

---

## Resumen Ejecutivo

De los **239 documentos sustantivos** con tema "CAMBIO CLIMÁTICO" en la aplicación actual, se excluyen **9 documentos** según las instrucciones de los expertos, resultando en **230 documentos** para la segunda fase. Además, se agregan **14 publicaciones** adicionales (Período de Sesiones de CEPAL y Foro Regional sobre Desarrollo Sostenible), para un **total final de 244 documentos**.

| Concepto | Cantidad |
|----------|----------|
| Base en app actual | 239 |
| Menos exclusiones | -9 |
| Más documentos nuevos | +14 |
| **Total segunda fase** | **244** |

---

## Documentos Excluidos por Categoría

### 1. ACUERDO REGIONAL (Versiones duplicadas) — 4 documentos

Se excluyen todas las versiones del Acuerdo Regional debido a duplicación en varios idiomas/formatos:

1. **Acuerdo Regional sobre el Acceso a la Información, la Participación Pública y el Acceso a la Justicia en Asuntos Ambientales en América Latina y el Caribe**

2. **Acuerdo Regional sobre el Acceso a la Información, la Participación Pública y el Acceso a la Justicia en Asuntos Ambientales en América Latina y el Caribe. Guía de implementación**

3. **Acuerdo Regional sobre el Acceso a la Información, la Participación Pública y el Acceso a la Justicia en Asuntos Ambientales en América Latina y el Caribe. Versión accesible**

4. **Ruta para la implementación del Acuerdo Regional sobre el Acceso a la Información, la Participación Pública y el Acceso a la Justicia en Asuntos Ambientales en América Latina y el Caribe en Chile**

---

### 2. VERSIONES ACCESIBLES — 2 documentos

Se excluyen versiones accesibles de documentos de CEPAL (no son la versión oficial):

5. **Estudio Económico de América Latina y el Caribe, 2023. Versión accesible**

6. **Estudio Económico de América Latina y el Caribe, 2024. Resumen ejecutivo. Versión accesible**

---

### 3. REVISTAS DE CEPAL — 3 documentos

Se excluyen revistas de CEPAL según recomendación de expertos: *"no se incluyen revistas ya que no todos los artículos son de autoría de CEPAL"*

7. **Revista CEPAL no.116**

8. **Revista CEPAL no. 129**

9. **Revista CEPAL no. 142**

---

## Documentos NO Encontrados en el Dataset

Se buscaron pero no se encontraron en los 239 documentos sustantivos:

- ✗ Catálogo de publicaciones de la División de Desarrollo Sostenible y Asentamientos Humanos
- ✗ Reglas de procedimiento del Acuerdo de Escazú
- ✗ The Hummingbird

---

## Documentos Agregados para Segunda Fase

Se agregan **14 publicaciones** según instrucciones de los expertos:

### Período de Sesiones de CEPAL (5 documentos)
1. América Latina y el Caribe ante las trampas del desarrollo: Transformaciones indispensables y cómo gestionarlas (2024)
2. Hacia la transformación del modelo de desarrollo en América Latina y el Caribe: producción, inclusión y sostenibilidad (2022)
3. Construir un nuevo futuro: una recuperación transformadora con igualdad y sostenibilidad (2020) — Handle: https://hdl.handle.net/11362/46682
4. La ineficiencia de la desigualdad (2018)
5. Horizontes 2030: la igualdad en el centro del desarrollo Sostenible (2016)

### Foro Regional sobre Desarrollo Sostenible (9 documentos)
6. Agenda 2030 en América Latina y el Caribe: ¿cómo acelerar el paso hacia su cumplimiento en la nueva era de incertidumbre y fragmentación geopolítica? (2026)
7. América Latina y el Caribe y la Agenda 2030 a cinco años de la meta: ¿cómo gestionar las transformaciones para acelerar el progreso? (2025)
8. América Latina y el Caribe ante el desafío de acelerar el paso hacia el cumplimiento de la Agenda 2030: transiciones hacia la sostenibilidad (2024)
9. América Latina y el Caribe en la mitad del camino hacia 2030: avances y propuestas de aceleración (2023)
10. Una década de acción para un cambio de época (2022) — Handle: https://hdl.handle.net/11362/47745
11. INFORME ANUAL DE PROGRESO: Construir un futuro mejor: acciones para fortalecer la Agenda 2030 para el Desarrollo Sostenible (2021)
12. Informe de avance cuatrienal sobre el progreso y los desafíos regionales de la Agenda 2030 para el Desarrollo Sostenible en América Latina y el Caribe (2019)
13. Segundo informe anual sobre el progreso y los desafíos regionales de la Agenda 2030 para el Desarrollo Sostenible en América Latina y el Caribe (2018)
14. Informe anual sobre el progreso y los desafíos regionales de la Agenda 2030 para el Desarrollo Sostenible en América Latina y el Caribe (2017)

---

## Implementación Técnica

### Ubicación del código
- **Archivo principal**: `segunda_fase.py`
- **Función de exclusión**: `excluir_documentos(df)`
- **Función de búsqueda**: `buscar_documento_inteligente(df, doc)`
- **Función de agregación**: `agregar_documentos(df_base)`

### Criterios de exclusión programados
1. Exclusión de títulos específicos (Acuerdo Regional)
2. Exclusión de patrón "accesible" en títulos
3. Exclusión de revistas (tipo_gr == "Boletines y Revistas")
4. Exclusión de otras revistas específicas (The Hummingbird, Catálogo de publicaciones)

### Vista en la aplicación
- **Pestaña**: "Documentos para 2da fase"
- **URL**: `/segunda-fase`
- **Ícono**: `:material/checklist:`
- **Funcionalidad**: Tabla interactiva con descarga en CSV

---

## Verificación

Scripts de verificación disponibles:
- `listar_excluidos.py` — Detalle de cada documento excluido
- `verificar_sustantivos.py` — Resumen de cambios
- `verificar_busqueda.py` — Verificación de búsqueda inteligente de documentos

**Ejecución**:
```bash
python listar_excluidos.py
```

---

## Notas Importantes

1. **División de Desarrollo Sostenible**: Se mantiene esta división en el análisis. Solo se excluyó el catálogo específico de publicaciones (que no fue encontrado en los 239 sustantivos).

2. **Búsqueda inteligente**: Los dos documentos faltantes ("Una década de acción para un cambio de época" y el "INFORME ANUAL DE PROGRESO") se encontraron con sus nombres completos del dataset original mediante búsqueda inteligente.

3. **Revistas**: Se excluyeron todas las revistas de CEPAL (tipo_gr = "Boletines y Revistas") siguiendo la recomendación de expertos.

4. **Versiones accesibles**: Se excluyeron solo las versiones explícitamente marcadas como "accesibles", no toda la división.

---

**Documento preparado por**: Sistema de depuración de documentos  
**Fecha de aprobación**: 2026-06-09  
**Estado**: ✅ Definitivo
