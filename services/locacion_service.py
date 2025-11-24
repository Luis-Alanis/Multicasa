from models.database import SessionLocal
from models.entities import Locacion
from models.repositories import LocacionRepository

class LocacionService:
    @staticmethod
    def obtener_todas():
        db = SessionLocal()
        try:
            return LocacionRepository.obtener_todas(db)
        finally:
            db.close()

    @staticmethod
    def obtener_por_id(id_locacion: int):
        db = SessionLocal()
        try:
            return LocacionRepository.obtener_por_id(db, id_locacion)
        finally:
            db.close()

    @staticmethod
    def crear(nombre: str):
        db = SessionLocal()
        try:
            return LocacionRepository.crear(db, nombre)
        finally:
            db.close()

    @staticmethod
    def actualizar(id_locacion: int, nombre: str):
        db = SessionLocal()
        try:
            return LocacionRepository.actualizar(db, id_locacion, nombre)
        finally:
            db.close()

    @staticmethod
    def eliminar(id_locacion: int):
        db = SessionLocal()
        try:
            return LocacionRepository.eliminar(db, id_locacion)
        finally:
            db.close()