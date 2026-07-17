"""Analisis puntual de costo por sesion (transcripts de Claude Code en disco).

No es parte del pipeline de Fase 2 -- es un script de una sola vez para responder
la pregunta del usuario sobre el costo del intento fallido de Workflow multiagente
(Ronda 7, 2026-07-14) vs. el enfoque uno-a-la-vez que le siguio.

Uso: python _analisis_costo_sesiones.py <directorio_de_sesiones> [--min-size-kb N]
"""
import json
import os
import sys
from collections import defaultdict

# Precios USD por millon de tokens (ver claude-api skill, cacheado 2026-06-24;
# cache write/read son multiplicadores documentados: 1.25x/2x/0.1x del precio de input).
PRECIOS = {
    "claude-fable-5": {"input": 10.00, "output": 50.00, "cache_5m": 12.50, "cache_1h": 20.00, "cache_read": 1.00},
    "claude-mythos-5": {"input": 10.00, "output": 50.00, "cache_5m": 12.50, "cache_1h": 20.00, "cache_read": 1.00},
    # Sonnet 5 tiene precio intro (2.00/10.00) vigente hasta 2026-08-31; hoy (2026-07-15) aplica.
    # PRECIOS_SONNET5_LISTA guarda el precio de lista por si hace falta comparar.
    "claude-sonnet-5": {"input": 2.00, "output": 10.00, "cache_5m": 2.50, "cache_1h": 4.00, "cache_read": 0.20},
    "claude-opus-4-8": {"input": 5.00, "output": 25.00, "cache_5m": 6.25, "cache_1h": 10.00, "cache_read": 0.50},
    "claude-haiku-4-5": {"input": 1.00, "output": 5.00, "cache_5m": 1.25, "cache_1h": 2.00, "cache_read": 0.10},
    "claude-opus-4-7": {"input": 5.00, "output": 25.00, "cache_5m": 6.25, "cache_1h": 10.00, "cache_read": 0.50},
    "claude-opus-4-6": {"input": 5.00, "output": 25.00, "cache_5m": 6.25, "cache_1h": 10.00, "cache_read": 0.50},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00, "cache_5m": 3.75, "cache_1h": 6.00, "cache_read": 0.30},
}

# Algunos modelos aparecen en los transcripts con sufijo de fecha (p.ej. claude-haiku-4-5-20251001);
# se normaliza quitando el sufijo "-YYYYMMDD" antes de buscar en PRECIOS.
import re as _re
_DATE_SUFFIX = _re.compile(r"-\d{8}$")


def _normalizar_modelo(model):
    if not model:
        return model
    return _DATE_SUFFIX.sub("", model)


def costo_usd(model, u):
    """u es el bucket YA AGREGADO (claves planas input_tokens/output_tokens/cache_5m/cache_1h/cache_read),
    no el objeto `usage` crudo del mensaje -- por eso NO se lee u["cache_creation"] aqui."""
    p = PRECIOS.get(_normalizar_modelo(model))
    if not p:
        return None
    return (
        u.get("input_tokens", 0) / 1e6 * p["input"]
        + u.get("output_tokens", 0) / 1e6 * p["output"]
        + u.get("cache_5m", 0) / 1e6 * p["cache_5m"]
        + u.get("cache_1h", 0) / 1e6 * p["cache_1h"]
        + u.get("cache_read", 0) / 1e6 * p["cache_read"]
    )


def analizar_archivo(ruta):
    """Recorre el jsonl linea por linea (streaming) y agrega usage por rama principal vs subagentes."""
    agg = {
        "principal": defaultdict(lambda: {"input_tokens": 0, "output_tokens": 0, "cache_5m": 0, "cache_1h": 0, "cache_read": 0}),
        "subagente": defaultdict(lambda: {"input_tokens": 0, "output_tokens": 0, "cache_5m": 0, "cache_1h": 0, "cache_read": 0}),
    }
    n_msgs_principal = 0
    n_msgs_subagente = 0
    n_task_tool_use = 0
    primer_ts = None
    ultimo_ts = None
    cwd = None

    with open(ruta, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue

            ts = d.get("timestamp")
            if ts:
                if primer_ts is None or ts < primer_ts:
                    primer_ts = ts
                if ultimo_ts is None or ts > ultimo_ts:
                    ultimo_ts = ts
            if cwd is None and d.get("cwd"):
                cwd = d["cwd"]

            if d.get("type") == "assistant":
                msg = d.get("message", {})
                model = msg.get("model")
                usage = msg.get("usage")
                if not usage or not model:
                    continue
                rama = "subagente" if d.get("isSidechain") else "principal"
                if rama == "principal":
                    n_msgs_principal += 1
                else:
                    n_msgs_subagente += 1
                cc = usage.get("cache_creation") or {}
                bucket = agg[rama][model]
                bucket["input_tokens"] += usage.get("input_tokens", 0)
                bucket["output_tokens"] += usage.get("output_tokens", 0)
                bucket["cache_5m"] += cc.get("ephemeral_5m_input_tokens", 0)
                bucket["cache_1h"] += cc.get("ephemeral_1h_input_tokens", 0)
                bucket["cache_read"] += usage.get("cache_read_input_tokens", 0)
                # contar tool_use de tipo Task (subagentes lanzados) en la rama principal
                if rama == "principal":
                    for block in msg.get("content", []) or []:
                        if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Task":
                            n_task_tool_use += 1

    return {
        "ruta": ruta,
        "cwd": cwd,
        "primer_ts": primer_ts,
        "ultimo_ts": ultimo_ts,
        "n_msgs_principal": n_msgs_principal,
        "n_msgs_subagente": n_msgs_subagente,
        "n_task_tool_use": n_task_tool_use,
        "agg": agg,
    }


def costo_total(agg):
    total = 0.0
    desconocido_tokens = 0
    for rama in agg.values():
        for model, u in rama.items():
            c = costo_usd(model, u)
            if c is None:
                desconocido_tokens += u["input_tokens"] + u["output_tokens"]
            else:
                total += c
    return total, desconocido_tokens


def encontrar_subagentes(directorio_sesion):
    """Busca recursivamente jsonl de subagentes/workflows bajo el directorio de una sesion (mismo nombre que el .jsonl principal, sin extension)."""
    subs = []
    if not os.path.isdir(directorio_sesion):
        return subs
    for root, _, files in os.walk(directorio_sesion):
        for fn in files:
            if fn.endswith(".jsonl"):
                subs.append(os.path.join(root, fn))
    return subs


def agregar_en(dest_agg, agg_fuente):
    for rama, modelos in agg_fuente.items():
        for model, u in modelos.items():
            b = dest_agg[rama][model]
            for k in ("input_tokens", "output_tokens", "cache_5m", "cache_1h", "cache_read"):
                b[k] += u[k]


def main():
    if len(sys.argv) < 2:
        print("Uso: python _analisis_costo_sesiones.py <directorio> [--min-size-kb N]")
        sys.exit(1)
    directorio = sys.argv[1]
    min_kb = 0
    if "--min-size-kb" in sys.argv:
        min_kb = int(sys.argv[sys.argv.index("--min-size-kb") + 1])

    archivos = [
        os.path.join(directorio, n) for n in os.listdir(directorio)
        if n.endswith(".jsonl") and os.path.isfile(os.path.join(directorio, n))
    ]
    archivos.sort(key=lambda p: os.path.getsize(p))

    resultados = []
    for ruta in archivos:
        size_kb = os.path.getsize(ruta) / 1024
        if size_kb < min_kb:
            continue
        r = analizar_archivo(ruta)

        # Subagentes/Workflow anidados bajo un directorio del mismo nombre que la sesion
        session_id = os.path.basename(ruta).replace(".jsonl", "")
        dir_sesion = os.path.join(directorio, session_id)
        sub_rutas = encontrar_subagentes(dir_sesion)
        agg_subagentes = {"principal": defaultdict(lambda: {"input_tokens": 0, "output_tokens": 0, "cache_5m": 0, "cache_1h": 0, "cache_read": 0}),
                           "subagente": defaultdict(lambda: {"input_tokens": 0, "output_tokens": 0, "cache_5m": 0, "cache_1h": 0, "cache_read": 0})}
        n_subagent_files = len(sub_rutas)
        subagent_msgs = 0
        for sr in sub_rutas:
            rs = analizar_archivo(sr)
            # todo lo que venga de un archivo de subagente cuenta como "subagente" independientemente de isSidechain interno
            for modelos in rs["agg"].values():
                for model, u in modelos.items():
                    b = agg_subagentes["subagente"][model]
                    for k in ("input_tokens", "output_tokens", "cache_5m", "cache_1h", "cache_read"):
                        b[k] += u[k]
            subagent_msgs += rs["n_msgs_principal"] + rs["n_msgs_subagente"]

        costo_ppal, desconocido_ppal = costo_total(r["agg"])
        costo_sub, desconocido_sub = costo_total(agg_subagentes)

        r["size_kb"] = size_kb
        r["costo_ppal_usd"] = costo_ppal
        r["costo_subagentes_usd"] = costo_sub
        r["costo_usd"] = costo_ppal + costo_sub
        r["tokens_modelo_desconocido"] = desconocido_ppal + desconocido_sub
        r["n_subagent_files"] = n_subagent_files
        r["subagent_msgs"] = subagent_msgs
        r["subagent_size_kb"] = sum(os.path.getsize(p) for p in sub_rutas) / 1024
        resultados.append(r)

    resultados.sort(key=lambda r: r["primer_ts"] or "")

    print(f"{'sesion':<38} {'inicio':<20} {'fin':<20} {'MB_ppal':>8} {'MB_sub':>8} {'msj_ppal':>8} {'#subag':>7} {'costo_ppal':>10} {'costo_subag':>11} {'costo_TOTAL':>11}")
    total_general = 0.0
    for r in resultados:
        nombre = os.path.basename(r["ruta"]).replace(".jsonl", "")
        total_general += r["costo_usd"]
        print(f"{nombre:<38} {str(r['primer_ts'])[:19]:<20} {str(r['ultimo_ts'])[:19]:<20} "
              f"{r['size_kb']/1024:>8.1f} {r['subagent_size_kb']/1024:>8.1f} {r['n_msgs_principal']:>8} "
              f"{r['n_subagent_files']:>7} {r['costo_ppal_usd']:>10.2f} {r['costo_subagentes_usd']:>11.2f} {r['costo_usd']:>11.2f}")
        if r["tokens_modelo_desconocido"]:
            print(f"    (!) {r['tokens_modelo_desconocido']} tokens de modelo no tabulado en PRECIOS, excluidos del costo)")
    print(f"\nTOTAL estimado (hilo principal + subagentes/workflows): ${total_general:.2f} USD  ({len(resultados)} sesiones)")

    # Volcado detallado por sesion y por rama/modelo, para el analisis fino
    print("\n=== Detalle por sesion (rama principal, por modelo) ===")
    for r in resultados:
        nombre = os.path.basename(r["ruta"]).replace(".jsonl", "")
        print(f"\n--- {nombre} (cwd={r['cwd']}) ---")
        for rama, modelos in r["agg"].items():
            for model, u in modelos.items():
                c = costo_usd(model, u)
                c_str = f"${c:.2f}" if c is not None else "modelo no tabulado"
                print(f"  [{rama:10s}] {model:20s} in={u['input_tokens']:>9} out={u['output_tokens']:>8} "
                      f"cache5m={u['cache_5m']:>9} cache1h={u['cache_1h']:>8} cacheread={u['cache_read']:>10}  -> {c_str}")


if __name__ == "__main__":
    main()
