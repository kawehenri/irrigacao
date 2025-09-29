from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict, Any

from src import db
from src.models.registro_models import Registro
from src.models.usuario_models import Usuario
from src.models.valvula_models import Valvulas


def serialize_registro(registro: Registro) -> Dict[str, Any]:
    """Convert a Registro model instance into a serializable dict."""
    return {
        "id": registro.id,
        "status": registro.status,
        "data_acionamento": (
            registro.data_acionamento.isoformat() if getattr(registro, "data_acionamento", None) else None
        ),
        "id_usuario": registro.id_usuario,
        "id_valvula": registro.id_valvula,
    }


def get_registro_by_id(registro_id: int) -> Optional[Registro]:
    """Fetch a single Registro by its primary key."""
    return Registro.query.get(registro_id)


def list_registros(limit: Optional[int] = None, offset: int = 0) -> List[Registro]:
    """Return a list of Registro rows, optionally paginated."""
    query = Registro.query.order_by(Registro.id.desc())
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return list(query.all())


def _assert_usuario_exists(usuario_id: int) -> None:
    if not Usuario.query.get(usuario_id):
        raise ValueError(f"Usuario id={usuario_id} não encontrado")


def _assert_valvula_exists(valvula_id: int) -> None:
    if not Valvulas.query.get(valvula_id):
        raise ValueError(f"Válvula id={valvula_id} não encontrada")


def create_registro(
    *,
    status: bool,
    data_acionamento: datetime,
    id_usuario: int,
    id_valvula: int,
) -> Registro:
    """Create and persist a new Registro row.

    Raises ValueError if related foreign keys do not exist.
    """
    _assert_usuario_exists(id_usuario)
    _assert_valvula_exists(id_valvula)

    novo_registro = Registro(
        status=status,
        data_acionamento=data_acionamento,
        id_usuario=id_usuario,
        id_valvula=id_valvula,
    )
    db.session.add(novo_registro)
    db.session.commit()
    return novo_registro


def update_registro(
    registro_id: int,
    *,
    status: Optional[bool] = None,
    data_acionamento: Optional[datetime] = None,
    id_usuario: Optional[int] = None,
    id_valvula: Optional[int] = None,
) -> Registro:
    """Update allowed fields of an existing Registro and persist the changes.

    Raises ValueError when the Registro or referenced foreign rows are not found.
    """
    registro = Registro.query.get(registro_id)
    if not registro:
        raise ValueError(f"Registro id={registro_id} não encontrado")

    if id_usuario is not None:
        _assert_usuario_exists(id_usuario)
        registro.id_usuario = id_usuario

    if id_valvula is not None:
        _assert_valvula_exists(id_valvula)
        registro.id_valvula = id_valvula

    if status is not None:
        registro.status = status

    if data_acionamento is not None:
        registro.data_acionamento = data_acionamento

    db.session.commit()
    return registro


def delete_registro(registro_id: int) -> bool:
    """Delete a Registro row. Returns True if a row was deleted, False otherwise."""
    registro = Registro.query.get(registro_id)
    if not registro:
        return False
    db.session.delete(registro)
    db.session.commit()
    return True

