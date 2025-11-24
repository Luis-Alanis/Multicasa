from models.database import SessionLocal
from models.entities import Casa
from models.repositories import CasaRepository

class CasaService:
    @staticmethod
    def obtener_todas(incluir_vendidas=False):
        db = SessionLocal()
        try:
            return CasaRepository.obtener_todas(db, incluir_vendidas=incluir_vendidas)
        finally:
            db.close()

    @staticmethod
    def obtener_por_id(id_casa: int):
        db = SessionLocal()
        try:
            return CasaRepository.obtener_por_id(db, id_casa)
        finally:
            db.close()

    @staticmethod
    def buscar_con_filtros(**filtros):
        db = SessionLocal()
        try:
            return CasaRepository.buscar_completo(db, **filtros)
        finally:
            db.close()

    @staticmethod
    def crear(data: dict):
        db = SessionLocal()
        try:
            return CasaRepository.crear(db, data)
        finally:
            db.close()

    @staticmethod
    def actualizar(id_casa: int, data: dict):
        db = SessionLocal()
        try:
            return CasaRepository.actualizar(db, id_casa, data)
        finally:
            db.close()

    @staticmethod
    def eliminar(id_casa: int):
        db = SessionLocal()
        try:
            return CasaRepository.eliminar(db, id_casa)
        finally:
            db.close()

    @staticmethod
    def obtener_estadisticas():
        db = SessionLocal()
        try:
            return CasaRepository.obtener_estadisticas(db)
        finally:
            db.close()