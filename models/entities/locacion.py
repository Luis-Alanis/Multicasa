from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.database import Base

class Locacion(Base):
    __tablename__ = 'catalogo_locacion'
    
    id_locacion = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), unique=True, nullable=False)
    
    casas = relationship('Casa', back_populates='locacion')
    
    def to_dict(self):
        return {
            'id_locacion': self.id_locacion,
            'nombre': self.nombre
        }