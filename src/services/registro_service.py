from models.registro_models import Registro
from src import db

def criar_registro(registro):
    registro_db = Registro(status=registro.status, dt_acionamento=registro.dt_acionamento, id_valvula=registro.id_valvula, id_usuario=registro.id_usuario)
    db.session.add(registro_db)
    db.session.commit()
    return registro_db

def listar_registro():
    registro_db = Registro.query.all()
    return registro_db

def listar_registro_id(id):
    registro_encontrado = Registro.query.get(id)
    try:
        if registro_encontrado:
            return registro_encontrado
    except Exception as e:
        return None
    
def atualizar_registro(id, dados):
    registro = Registro.query.get(id)
    if not registro:
        return None
    registro.status = dados.status
    registro.dt_acionamento = dados.dt_acionamento
    registro.id_valvula = dados.id_valvula
    registro.id_usuario = dados.id_usuario
    db.session.commit()
    return registro

def deletar_registro(id):
    registro = Registro.query.get(id)
    if not registro:
        return None
    db.session.delete(registro)
    db.session.commit()
    return registro

