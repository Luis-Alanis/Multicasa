from sqlalchemy.orm import Session
from models.entities import Admin

class AdminRepository:
    """Repositorio para operaciones de base de datos de Admins"""
    
    @staticmethod
    def crear(db: Session, data: dict):
        nuevo = Admin(**data)
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo.to_dict()
    
    @staticmethod
    def actualizar(db: Session, id_admin: int, data: dict):
        admin = db.query(Admin).filter(Admin.id_admin == id_admin).first()
        if not admin:
            return None
        for k, v in data.items():
            if hasattr(admin, k) and v is not None:
                setattr(admin, k, v)
        db.commit()
        db.refresh(admin)
        return admin.to_dict()
    
    @staticmethod
    def eliminar(db: Session, id_admin: int):
        admin = db.query(Admin).filter(Admin.id_admin == id_admin).first()
        if admin:
            db.delete(admin)
            db.commit()
            return True
        return False
    
    @staticmethod
    def obtener_por_correo(db: Session, correo: str):
        admin = db.query(Admin).filter(Admin.correo == correo).first()
        return admin.to_dict() if admin else None
    
    @staticmethod
    def verificar_credenciales(db: Session, correo: str, contraseña: str):
        admin = db.query(Admin).filter(
            Admin.correo == correo,
            Admin.contraseña == contraseña
        ).first()
        return admin.to_dict() if admin else None