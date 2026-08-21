# Instrucciones del Proyecto - Enriquecimiento Fase 2

Este archivo contiene los estándares y flujos de trabajo acordados para este repositorio. El agente debe consultar este archivo al iniciar cualquier sesión de procesamiento masivo.

## 1. Configuración del Modelo
- **Modelo Predeterminado**: `gemini-3.7-flash` (configurado en `.gemini/settings.json`).
- **Verificación**: `ui.showModelInfoInChat` debe estar en `true` para confirmar visualmente el modelo en cada respuesta.
- **Routing**: `general.plan.modelRouting` debe estar en `false` para evitar fallbacks automáticos a modelos inferiores.

## 2. Flujo de Enriquecimiento en Paralelo
Para procesar múltiples documentos simultáneamente de forma segura, se utiliza el método de **Aislamiento de Sesión**:

### Lanzamiento Automático
Se deben utilizar scripts (Python o PowerShell) para lanzar instancias independientes del Gemini CLI con las siguientes características:
1.  **Bypass de Seguridad**: `$env:GEMINI_CLI_TRUST_WORKSPACE='true'` y flag `--skip-trust`.
2.  **Modo Autónomo**: Flag `--yolo` para ejecución de herramientas sin interrupciones.
3.  **Prompt Directo**: Flag `-i (Get-Content prompt.md -Raw)` para evitar bloqueos de tubería (pipes) en Windows.

### Ejemplo de Comando de Lanzamiento (PowerShell)
```powershell
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$pwd'; `$env:GEMINI_CLI_TRUST_WORKSPACE='true'; gemini --skip-trust --yolo -i (Get-Content 'temp_prompt_XXXXX.md' -Raw)"
```

## 3. Procesamiento de Documentos Extensos
Los documentos de más de 100 páginas siguen un flujo de 3 fases:
1.  **Fase 1 (Mapeo)**: Ejecutar `PROMPT_ID_INDICE_MAPA.md` para generar `indice_fuente.json` y `mapa_cortes_ID.md`.
2.  **Fase 2 (Parciales)**: Lanzar sesiones paralelas (máximo 2-3 simultáneas) usando `PROMPT_ID_PARCIAL_TEMPLATE.md` para cada bloque definido en el mapa.
3.  **Fase 3 (Consolidación)**: Ejecutar `PROMPT_ID_CONSOLIDACION.md` para unir los parciales y correr el pipeline de validación.

## 4. Estándares Técnicos del JSON
- **Orden de Claves**: `documento` -> `resumen_enriquecido` -> `resumen_secciones` -> `interpelacion` -> `tipologia`.
- **Dimensiones**: Deben contener solo `dimension`, `cita` (literal exacta) y `pagina`.
- **Jerarquía**: Nivel 1 (Capítulos), Nivel 2 (Introducciones de capítulo y secciones A, B, C...), Nivel 3 (Subsecciones 1, 2, 3...).
- **Limpieza**: Ejecutar `pipeline/canonical_fixer.py` antes de cualquier promoción a `corpus/resultados/`.
