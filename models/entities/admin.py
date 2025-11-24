from sqlalchemy import Column, Integer, String
from models.database import Base

class Admin(Base):
    __tablename__ = 'admins'
    
    id_admin = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(120), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    
    def to_dict(self):
        return {
            'id_admin': self.id_admin,
            'nombre': self.nombre,
            'correo': self.correo
        }