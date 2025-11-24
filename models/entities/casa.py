from sqlalchemy import Column, Integer, String, Numeric, Enum, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from models.database import Base
import json

class Casa(Base):
    __tablename__ = 'casas'
    
    id_casa = Column(Integer, primary_key=True, autoincrement=True)
    id_locacion = Column(Integer, ForeignKey('catalogo_locacion.id_locacion'), nullable=False)
    latitud = Column(Numeric(10, 6), nullable=False)
    longitud = Column(Numeric(10, 6), nullable=False)
    codigo_postal = Column(String(10))
    costo = Column(Numeric(12, 2), nullable=False)
    recamaras = Column(Integer, nullable=False)
    baños = Column(Integer, nullable=False)
    estatus_venta = Column(Enum('En Venta', 'Vendida'), default='En Venta', nullable=False)
    fotos = Column(Text)
    
    locacion = relationship('Locacion', back_populates='casas')
    
    __table_args__ = (
        Index('idx_locacion', 'id_locacion'),
        Index('idx_codigo_postal', 'codigo_postal'),
        Index('idx_estatus_venta', 'estatus_venta'),
        Index('idx_costo', 'costo'),
    )
    
    def to_dict(self):
        fotos_list = []
        if self.fotos:
            try:
                fotos_list = json.loads(self.fotos)
            except:
                pass
        
        fotos_procesadas = []
        if fotos_list and len(fotos_list) > 0:
            for foto in fotos_list:
                if not foto:
                    continue
                    
                if foto.startswith('images/'):
                    fotos_procesadas.append(foto)
                elif foto.startswith('http://') or foto.startswith('https://'):
                    fotos_procesadas.append(foto)
                else:
                    fotos_procesadas.append(f'images/casas/{foto}')
        
        if not fotos_procesadas:
            fotos_procesadas = ['images/no-image.jpg']
        
        foto_principal = fotos_procesadas[0] if fotos_procesadas else 'images/no-image.jpg'
        
        return {
            'id_casa': self.id_casa,
            'id_locacion': self.id_locacion,
            'locacion': self.locacion.nombre if self.locacion else None,
            'latitud': float(self.latitud) if self.latitud else None,
            'longitud': float(self.longitud) if self.longitud else None,
            'codigo_postal': self.codigo_postal,
            'costo': float(self.costo),
            'recamaras': self.recamaras,
            'baños': self.baños,
            'estatus_venta': self.estatus_venta,
            'fotos': fotos_procesadas,
            'fotos_lista': fotos_procesadas,
            'foto_principal': foto_principal
        }