from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.entities import Usuario

class UsuarioRepository:
    """Repositorio para operaciones de base de datos de Usuarios"""
    
    @staticmethod
    def obtener_todos(db: Session):
        usuarios = db.query(Usuario).all()
        return [usuario.to_dict() for usuario in usuarios]
    
    @staticmethod
    def obtener_por_id(db: Session, id_usuario: int):
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        return usuario.to_dict() if usuario else None
    
    @staticmethod
    def crear(db: Session, data: dict):
        nuevo_usuario = Usuario(**data)
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario.to_dict()
    
    @staticmethod
    def actualizar(db: Session, id_usuario: int, data: dict):
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if usuario:
            for key, value in data.items():
                if hasattr(usuario, key) and value is not None:
                    setattr(usuario, key, value)
            db.commit()
            db.refresh(usuario)
            return usuario.to_dict()
        return None
    
    @staticmethod
    def eliminar(db: Session, id_usuario: int):
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if usuario:
            db.delete(usuario)
            db.commit()
            return True
        return False
    
    @staticmethod
    def buscar(db: Session, texto: str):
        if not texto:
            return []
        like = f"%{texto}%"
        q = db.query(Usuario).filter(
            or_(
                Usuario.nombre.like(like),
                Usuario.correo.like(like),
                Usuario.telefono.like(like),
                Usuario.asunto.like(like),
                Usuario.mensaje.like(like)
            )
        )
        return [u.to_dict() for u in q.all()]