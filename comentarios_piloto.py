"""
Persistencia de comentarios del revisor sobre las 17 publicaciones del piloto.

Sigue el mismo patrón dual de seleccion.py (local JSON / GitHub) pero
independiente, para no mezclar marcas de inclusión con comentarios de revisión.
"""

from __future__ import annotations

import base64
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol

import streamlit as st

DIR_PILOT = Path(__file__).resolve().parent / "fase2" / "pilot"
ARCHIVO_LOCAL = DIR_PILOT / "comentarios_revision.json"
RUTA_REMOTA_DEFECTO = "fase2/pilot/comentarios_revision.json"
RAMA_DEFECTO = "main"
MENSAJE_COMMIT = "chore(piloto): actualizar comentarios de revisión"


@dataclass
class ComentarioRevisor:
    comentario: str = ""
    ultima_modificacion: str = ""


class _Store(Protocol):
    def cargar(self) -> dict[str, ComentarioRevisor]: ...
    def guardar(self, estado: dict[str, ComentarioRevisor]) -> None: ...
    def etiqueta(self) -> str: ...


def _ahora_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _dict_a_comentarios(datos: dict) -> dict[str, ComentarioRevisor]:
    estado: dict[str, ComentarioRevisor] = {}
    if not isinstance(datos, dict):
        return estado
    for key, valor in datos.items():
        if not isinstance(valor, dict):
            continue
        estado[str(key)] = ComentarioRevisor(
            comentario=str(valor.get("comentario", "")),
            ultima_modificacion=str(valor.get("ultima_modificacion", "")),
        )
    return estado


def _comentarios_a_dict(estado: dict[str, ComentarioRevisor]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for key, c in estado.items():
        if not c.comentario.strip():
            continue
        out[key] = asdict(c)
    return out


@dataclass
class LocalJSONStore:
    ruta: Path = ARCHIVO_LOCAL

    def cargar(self) -> dict[str, ComentarioRevisor]:
        if not self.ruta.exists():
            return {}
        try:
            datos = json.loads(self.ruta.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        return _dict_a_comentarios(datos)

    def guardar(self, estado: dict[str, ComentarioRevisor]) -> None:
        payload = json.dumps(_comentarios_a_dict(estado), ensure_ascii=False, indent=2)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
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
    _sha_cache: str | None = None

    def _repo(self):
        from github import Auth, Github
        gh = Github(auth=Auth.Token(self.token))
        return gh.get_repo(self.repo)

    def cargar(self) -> dict[str, ComentarioRevisor]:
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
        return _dict_a_comentarios(datos)

    def guardar(self, estado: dict[str, ComentarioRevisor]) -> None:
        from github import GithubException
        payload = json.dumps(_comentarios_a_dict(estado), ensure_ascii=False, indent=2)
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
                path=self.path, message=MENSAJE_COMMIT,
                content=payload, branch=self.branch,
            )
            self._sha_cache = res["content"].sha
        else:
            res = repo.update_file(
                path=self.path, message=MENSAJE_COMMIT,
                content=payload, sha=self._sha_cache, branch=self.branch,
            )
            self._sha_cache = res["content"].sha

    def etiqueta(self) -> str:
        return f"GitHub: `{self.repo}` · `{self.path}` · rama `{self.branch}`"


@st.cache_resource(show_spinner=False)
def _store_actual() -> _Store:
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


def cargar_comentarios() -> dict[str, ComentarioRevisor]:
    if "comentarios_piloto_estado" not in st.session_state:
        estado = _store_actual().cargar()
        st.session_state["comentarios_piloto_estado"] = estado
    return st.session_state["comentarios_piloto_estado"]


def guardar_comentario(doc_id: str, comentario: str) -> ComentarioRevisor:
    estado = cargar_comentarios()
    c = ComentarioRevisor(comentario=comentario.strip(), ultima_modificacion=_ahora_iso())
    nuevo = dict(estado)
    if not c.comentario.strip():
        nuevo.pop(doc_id, None)
    else:
        nuevo[doc_id] = c
    _store_actual().guardar(nuevo)
    estado.clear()
    estado.update(nuevo)
    return c


def comentario_de(doc_id: str) -> ComentarioRevisor:
    return cargar_comentarios().get(doc_id, ComentarioRevisor())
