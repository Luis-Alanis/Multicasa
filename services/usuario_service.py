from models.database import SessionLocal
from models.entities import Usuario
from models.repositories import UsuarioRepository

class UsuarioService:
    @staticmethod
    def obtener_todos():
        db = SessionLocal()
        try:
            return UsuarioRepository.obtener_todos(db)
        finally:
            db.close()

    @staticmethod
    def obtener_por_id(id_usuario: int):
        db = SessionLocal()
        try:
            return UsuarioRepository.obtener_por_id(db, id_usuario)
        finally:
            db.close()

    @staticmethod
    def crear(data: dict):
        db = SessionLocal()
        try:
            return UsuarioRepository.crear(db, data)
        finally:
            db.close()

    @staticmethod
    def actualizar(id_usuario: int, data: dict):
        db = SessionLocal()
        try:
            return UsuarioRepository.actualizar(db, id_usuario, data)
        finally:
            db.close()

    @staticmethod
    def eliminar(id_usuario: int):
        db = SessionLocal()
        try:
            return UsuarioRepository.eliminar(db, id_usuario)
        finally:
            db.close()

    @staticmethod
    def buscar(texto: str):
        db = SessionLocal()
        try:
            return UsuarioRepository.buscar(db, texto)
        finally:
            db.close()