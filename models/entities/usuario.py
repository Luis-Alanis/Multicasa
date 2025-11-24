from sqlalchemy import Column, Integer, String, Text
from models.database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(120), nullable=False)
    telefono = Column(String(20))
    asunto = Column(String(100))
    mensaje = Column(Text)
    estado = Column(String(20), default='pendiente')
    
    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'correo': self.correo,
            'telefono': self.telefono,
            'asunto': self.asunto,
            'mensaje': self.mensaje,
            'estado': self.estado
        }