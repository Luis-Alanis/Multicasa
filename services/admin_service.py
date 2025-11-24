from models.database import SessionLocal
from models.entities import Admin
from models.repositories import AdminRepository

class AdminService:
    @staticmethod
    def verificar_credenciales(correo: str, contraseña: str):
        db = SessionLocal()
        try:
            return AdminRepository.verificar_credenciales(db, correo, contraseña)
        finally:
            db.close()

    @staticmethod
    def crear(data: dict):
        db = SessionLocal()
        try:
            return AdminRepository.crear(db, data)
        finally:
            db.close()

    @staticmethod
    def eliminar(id_admin: int):
        db = SessionLocal()
        try:
            return AdminRepository.eliminar(db, id_admin)
        finally:
            db.close()