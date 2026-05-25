"""
Persistencia de la selección de revisión (Incluir + nota por publicación).

Backends:
- GitHub (lee/escribe un JSON en el repo vía PyGithub) — para Streamlit Cloud.
- JSON local — fallback de desarrollo cuando no hay secrets configurados.

Selección automática: si existe `st.secrets["github"]` con `token` y `repo`,
se usa GitHubStore; si no, LocalJSONStore en `seleccion_revision.json`
de esta carpeta.
"""

from __future__ import annotations

import base64
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Protocol

import streamlit as st

DIR = Path(__file__).resolve().parent
ARCHIVO_LOCAL = DIR / "seleccion_revision.json"
RUTA_REMOTA_DEFECTO = "seleccion_revision.json"
RAMA_DEFECTO = "main"
MENSAJE_COMMIT = "chore(revision): actualizar selección cambio climático"


@dataclass
class MarcaSeleccion:
    incluir: bool = False
    nota: str = ""
    marcado_en: str = ""

    def vacio(self) -> bool:
        return not self.incluir and not self.nota.strip()


def _ahora_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


class _Store(Protocol):
    def cargar(self) -> dict[str, MarcaSeleccion]: ...
    def guardar(self, estado: dict[str, MarcaSeleccion]) -> None: ...
    def etiqueta(self) -> str: ...


@dataclass
class LocalJSONStore:
    ruta: Path = ARCHIVO_LOCAL

    def cargar(self) -> dict[str, MarcaSeleccion]:
        if not self.ruta.exists():
            return {}
        try:
            datos = json.loads(self.ruta.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        return _dict_a_marcas(datos)

    def guardar(self, estado: dict[str, MarcaSeleccion]) -> None:
        payload = json.dumps(_marcas_a_dict(estado), ensure_ascii=False, indent=2)
        tmp = self.ruta.with_suffix(".tmp")
        tmp.write_text(payload, encoding="utf-8")
        tmp.replace(self.ruta)

    def etiqueta(self) -> str:
        return f"local: `{self.ruta.name}`"


@dataclass
class GitHubStore:
    token: str
    repo: str
    path: str = RUTA_REMOTA_DEFECTO
    branch: str = RAMA_DEFECTO
    _sha_cache: str | None = field(default=None, init=False, repr=False)

    def _repo(self):
        from github import Auth, Github

        gh = Github(auth=Auth.Token(self.token))
        return gh.get_repo(self.repo)

    def cargar(self) -> dict[str, MarcaSeleccion]:
        from github import GithubException

        try:
            contenido = self._repo().get_contents(self.path, ref=self.branch)
        except GithubException as exc:
            if exc.status == 404:
                self._sha_cache = None
                return {}
            raise
        self._sha_cache = contenido.sha
        raw = base64.b64decode(contenido.content).decode("utf-8")
        try:
            datos = json.loads(raw)
        except json.JSONDecodeError:
            return {}
        return _dict_a_marcas(datos)

    def guardar(self, estado: dict[str, MarcaSeleccion]) -> None:
        from github import GithubException

        payload = json.dumps(_marcas_a_dict(estado), ensure_ascii=False, indent=2)
        repo = self._repo()
        if self._sha_cache is None:
            try:
                actual = repo.get_contents(self.path, ref=self.branch)
                self._sha_cache = actual.sha
            except GithubException as exc:
                if exc.status != 404:
                    raise
                self._sha_cache = None

        if self._sha_cache is None:
            res = repo.create_file(
                path=self.path,
                message=MENSAJE_COMMIT,
                content=payload,
                branch=self.branch,
            )
            self._sha_cache = res["content"].sha
        else:
            res = repo.update_file(
                path=self.path,
                message=MENSAJE_COMMIT,
                content=payload,
                sha=self._sha_cache,
                branch=self.branch,
            )
            self._sha_cache = res["content"].sha

    def etiqueta(self) -> str:
        return f"GitHub: `{self.repo}` · `{self.path}` · rama `{self.branch}`"


def _marcas_a_dict(estado: dict[str, MarcaSeleccion]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for uri, marca in estado.items():
        if marca.vacio():
            continue
        out[uri] = asdict(marca)
    return out


def _dict_a_marcas(datos: dict) -> dict[str, MarcaSeleccion]:
    estado: dict[str, MarcaSeleccion] = {}
    if not isinstance(datos, dict):
        return estado
    for uri, valor in datos.items():
        if not isinstance(valor, dict):
            continue
        estado[str(uri)] = MarcaSeleccion(
            incluir=bool(valor.get("incluir", False)),
            nota=str(valor.get("nota", "")),
            marcado_en=str(valor.get("marcado_en", "")),
        )
    return estado


@st.cache_resource(show_spinner=False)
def _store_actual() -> _Store:
    """Devuelve el backend de persistencia activo. Cacheado en proceso."""
    cfg = _leer_config_github()
    if cfg is not None:
        return GitHubStore(**cfg)
    return LocalJSONStore()


def _leer_config_github() -> dict | None:
    try:
        secrets = st.secrets
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return None
    if "github" not in secrets:
        return None
    bloque = secrets["github"]
    token = bloque.get("token") if isinstance(bloque, dict) else getattr(bloque, "get", lambda *_: None)("token")
    repo = bloque.get("repo") if isinstance(bloque, dict) else getattr(bloque, "get", lambda *_: None)("repo")
    if not token or not repo:
        return None
    cfg = {"token": token, "repo": repo}
    path = bloque.get("path") if isinstance(bloque, dict) else None
    branch = bloque.get("branch") if isinstance(bloque, dict) else None
    if path:
        cfg["path"] = path
    if branch:
        cfg["branch"] = branch
    return cfg


def store_etiqueta() -> str:
    return _store_actual().etiqueta()


def cargar_seleccion() -> dict[str, MarcaSeleccion]:
    """Carga el estado actual desde el backend (cacheado en session_state)."""
    if "seleccion_estado" not in st.session_state:
        st.session_state["seleccion_estado"] = _store_actual().cargar()
    return st.session_state["seleccion_estado"]


def actualizar_marca(uri: str, incluir: bool, nota: str) -> MarcaSeleccion:
    """Persiste primero al backend; solo si tuvo éxito muta el session_state."""
    estado = cargar_seleccion()
    marca = MarcaSeleccion(
        incluir=incluir,
        nota=nota.strip(),
        marcado_en=_ahora_iso(),
    )
    nuevo = dict(estado)
    if marca.vacio():
        nuevo.pop(uri, None)
    else:
        nuevo[uri] = marca
    _store_actual().guardar(nuevo)
    estado.clear()
    estado.update(nuevo)
    return marca


def aplicar_cambios_lote(cambios: dict[str, bool]) -> int:
    """
    Aplica varias marcas (uri -> incluir) y persiste con UNA sola escritura.
    Conserva la nota previa si existe. Devuelve la cantidad de marcas
    efectivamente modificadas.
    """
    if not cambios:
        return 0
    estado = cargar_seleccion()
    nuevo = dict(estado)
    timestamp = _ahora_iso()
    n_efectivos = 0
    for uri, incluir in cambios.items():
        marca_actual = nuevo.get(uri, MarcaSeleccion())
        if marca_actual.incluir == incluir and uri in nuevo:
            continue
        marca = MarcaSeleccion(
            incluir=bool(incluir),
            nota=marca_actual.nota,
            marcado_en=timestamp,
        )
        if marca.vacio():
            if nuevo.pop(uri, None) is not None:
                n_efectivos += 1
        else:
            nuevo[uri] = marca
            n_efectivos += 1
    if n_efectivos == 0:
        return 0
    _store_actual().guardar(nuevo)
    estado.clear()
    estado.update(nuevo)
    return n_efectivos


def marca_de(uri: str) -> MarcaSeleccion:
    return cargar_seleccion().get(uri, MarcaSeleccion())


def total_incluidos() -> int:
    return sum(1 for m in cargar_seleccion().values() if m.incluir)


def uris_incluidas() -> set[str]:
    return {uri for uri, m in cargar_seleccion().items() if m.incluir}
