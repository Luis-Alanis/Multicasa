from sqlalchemy.orm import Session
from models.entities import Locacion

class LocacionRepository:
    """Repositorio para operaciones de base de datos de Locaciones"""
    
    @staticmethod
    def obtener_todas(db: Session):
        locaciones = db.query(Locacion).all()
        return [loc.to_dict() for loc in locaciones]
    
    @staticmethod
    def obtener_por_id(db: Session, id_locacion: int):
        locacion = db.query(Locacion).filter(Locacion.id_locacion == id_locacion).first()
        return locacion.to_dict() if locacion else None
    
    @staticmethod
    def crear(db: Session, nombre: str):
        nueva_locacion = Locacion(nombre=nombre)
        db.add(nueva_locacion)
        db.commit()
        db.refresh(nueva_locacion)
        return nueva_locacion.to_dict()
    
    @staticmethod
    def actualizar(db: Session, id_locacion: int, nombre: str):
        locacion = db.query(Locacion).filter(Locacion.id_locacion == id_locacion).first()
        if locacion:
            locacion.nombre = nombre
            db.commit()
            db.refresh(locacion)
            return locacion.to_dict()
        return None
    
    @staticmethod
    def eliminar(db: Session, id_locacion: int):
        locacion = db.query(Locacion).filter(Locacion.id_locacion == id_locacion).first()
        if locacion:
            db.delete(locacion)
            db.commit()
            return True
        return False
    
    @staticmethod
    def buscar(db: Session, texto: str):
        if not texto:
            return []
        like = f"%{texto}%"
        q = db.query(Locacion).filter(Locacion.nombre.like(like))
        return [l.to_dict() for l in q.all()]