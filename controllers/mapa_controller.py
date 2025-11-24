from flask import Blueprint, jsonify, request
from models.database import SessionLocal
from models.repositories import CasaRepository
from services.casa_service import CasaService

mapa_bp = Blueprint('mapa_bp', __name__)

def get_db():
    """Helper para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass

@mapa_bp.route('/casas/mapa', methods=['GET'])
def mapa_casas():
    """Obtener casas para mostrar en el mapa (solo en venta para usuarios)"""
    filtros = {
        'ubicacion': request.args.get('ubicacion'),
        'precio_min': request.args.get('precioMin', type=float),
        'precio_max': request.args.get('precioMax', type=float),
        'recamaras': request.args.get('recamaras'),
        'baños': request.args.get('baños'),
        'user_lat': request.args.get('user_lat', type=float),
        'user_lon': request.args.get('user_lon', type=float),
        'rango_km': request.args.get('rango_km', type=float),
        'incluir_vendidas': False
    }
    filtros = {k: v for k, v in filtros.items() if v}
    resultados = CasaService.buscar_con_filtros(**filtros)
    return jsonify(resultados)

@mapa_bp.route('/admin/casas/mapa', methods=['GET'])
def mapa_casas_admin():
    """Obtener todas las casas para el mapa del admin (incluye vendidas)"""
    filtros = {
        'ubicacion': request.args.get('ubicacion'),
        'precio_min': request.args.get('precioMin', type=float),
        'precio_max': request.args.get('precioMax', type=float),
        'recamaras': request.args.get('recamaras'),
        'baños': request.args.get('baños'),
        'user_lat': request.args.get('user_lat', type=float),
        'user_lon': request.args.get('user_lon', type=float),
        'rango_km': request.args.get('rango_km', type=float),
        'incluir_vendidas': True
    }
    filtros = {k: v for k, v in filtros.items() if v}
    resultados = CasaService.buscar_con_filtros(**filtros)
    return jsonify(resultados)
