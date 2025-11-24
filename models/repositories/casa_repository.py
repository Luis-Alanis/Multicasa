from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from models.entities import Casa, Locacion
from math import radians, cos, sin, asin, sqrt
import json

class CasaRepository:
    """Repositorio para operaciones de base de datos de Casas"""
    
    @staticmethod
    def obtener_todas(db: Session, incluir_vendidas=False):
        query = db.query(Casa)
        if not incluir_vendidas:
            query = query.filter(Casa.estatus_venta == 'En Venta')
        return [casa.to_dict() for casa in query.all()]
    
    @staticmethod
    def obtener_por_id(db: Session, id_casa: int):
        casa = db.query(Casa).filter(Casa.id_casa == id_casa).first()
        return casa.to_dict() if casa else None
    
    @staticmethod
    def crear(db: Session, data: dict):
        fotos_json = json.dumps(data.get('fotos', []))
        
        nueva_casa = Casa(
            id_locacion=data['id_locacion'],
            latitud=data['latitud'],
            longitud=data['longitud'],
            codigo_postal=data.get('codigo_postal'),
            costo=data['costo'],
            recamaras=data['recamaras'],
            baños=data['baños'],
            estatus_venta=data.get('estatus_venta', 'En Venta'),
            fotos=fotos_json
        )
        
        db.add(nueva_casa)
        db.commit()
        db.refresh(nueva_casa)
        return nueva_casa.to_dict()
    
    @staticmethod
    def actualizar(db: Session, id_casa: int, data: dict):
        casa = db.query(Casa).filter(Casa.id_casa == id_casa).first()
        if not casa:
            return None
        
        if 'fotos' in data:
            data['fotos'] = json.dumps(data['fotos'])
        
        for key, value in data.items():
            if hasattr(casa, key):
                setattr(casa, key, value)
        
        db.commit()
        db.refresh(casa)
        return casa.to_dict()
    
    @staticmethod
    def eliminar(db: Session, id_casa: int):
        casa = db.query(Casa).filter(Casa.id_casa == id_casa).first()
        if casa:
            db.delete(casa)
            db.commit()
            return True
        return False
    
    @staticmethod
    def buscar(db: Session, texto: str):
        query = db.query(Casa).join(Locacion)
        query = query.filter(
            or_(
                Locacion.nombre.like(f'%{texto}%'),
                Casa.codigo_postal.like(f'%{texto}%')
            )
        )
        return [casa.to_dict() for casa in query.all()]
    
    @staticmethod
    def buscar_completo(db: Session, **filtros):
        query = db.query(Casa).join(Locacion)
        
        if not filtros.get('incluir_vendidas', False):
            query = query.filter(Casa.estatus_venta == 'En Venta')
        
        if filtros.get('ubicacion'):
            ubicacion = filtros['ubicacion']
            query = query.filter(
                or_(
                    Locacion.nombre.like(f'%{ubicacion}%'),
                    Casa.codigo_postal.like(f'%{ubicacion}%')
                )
            )
        
        if filtros.get('precio_min'):
            query = query.filter(Casa.costo >= filtros['precio_min'])
        if filtros.get('precio_max'):
            query = query.filter(Casa.costo <= filtros['precio_max'])
        
        if filtros.get('recamaras'):
            if filtros['recamaras'] == '4+':
                query = query.filter(Casa.recamaras >= 4)
            else:
                query = query.filter(Casa.recamaras == int(filtros['recamaras']))
        
        if filtros.get('baños'):
            if filtros['baños'] == '3+':
                query = query.filter(Casa.baños >= 3)
            else:
                query = query.filter(Casa.baños == int(filtros['baños']))
        
        casas = [casa.to_dict() for casa in query.all()]
        
        if filtros.get('rango_km') and filtros.get('user_lat') and filtros.get('user_lon'):
            casas = CasaRepository._filtrar_por_distancia(
                casas,
                float(filtros['user_lat']),
                float(filtros['user_lon']),
                float(filtros['rango_km'])
            )
        
        return casas
    
    @staticmethod
    def _filtrar_por_distancia(casas, user_lat, user_lon, rango_km):
        casas_filtradas = []
        
        for casa in casas:
            if casa['latitud'] and casa['longitud']:
                dist = CasaRepository._calcular_distancia(
                    user_lat, user_lon,
                    casa['latitud'], casa['longitud']
                )
                if dist <= rango_km:
                    casa['distancia'] = round(dist, 2)
                    casas_filtradas.append(casa)
        
        casas_filtradas.sort(key=lambda x: x.get('distancia', float('inf')))
        return casas_filtradas
    
    @staticmethod
    def _calcular_distancia(lat1, lon1, lat2, lon2):
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km
    
    @staticmethod
    def obtener_para_mapa(db: Session, solo_en_venta=True):
        query = db.query(Casa).filter(
            Casa.latitud.isnot(None),
            Casa.longitud.isnot(None)
        )
        
        if solo_en_venta:
            query = query.filter(Casa.estatus_venta == 'En Venta')
        
        return [casa.to_dict() for casa in query.all()]
    
    @staticmethod
    def obtener_estadisticas(db: Session):
        total = db.query(func.count(Casa.id_casa)).scalar()
        en_venta = db.query(func.count(Casa.id_casa)).filter(Casa.estatus_venta == 'En Venta').scalar()
        vendidas = total - en_venta
        
        precio_promedio = db.query(func.avg(Casa.costo)).scalar()
        precio_promedio = float(precio_promedio) if precio_promedio else 0
        
        return {
            'total_casas': total,
            'en_venta': en_venta,
            'vendidas': vendidas,
            'precio_promedio': precio_promedio
        }