from flask import Blueprint, render_template, request
from models.database import SessionLocal
from models.repositories import CasaRepository, LocacionRepository, AdminRepository, UsuarioRepository
from services.casa_service import CasaService
from services.locacion_service import LocacionService
from services.admin_service import AdminService
from services.usuario_service import UsuarioService

casa_bp = Blueprint('casa_bp', __name__)

def get_db():
    """Helper para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass

@casa_bp.route('/casas/buscar', methods=['GET'])
def buscar_casas():
    """Búsqueda de casas con filtros"""
    filtros = {
        'ubicacion': request.args.get('ubicacion'),
        'precio_min': request.args.get('precioMin'),
        'precio_max': request.args.get('precioMax'),
        'recamaras': request.args.get('recamaras'),
        'baños': request.args.get('baños'),
        'user_lat': request.args.get('user_lat'),
        'user_lon': request.args.get('user_lon'),
        'rango_km': request.args.get('rango_km'),
        'incluir_vendidas': False
    }
    filtros = {k: v for k, v in filtros.items() if v}
    resultados = CasaService.buscar_con_filtros(**filtros)
    return render_template('search.html', resultados=resultados, **request.args)

@casa_bp.route('/casas/detalles/<int:id_casa>', methods=['GET'])
def detalles_casa(id_casa):
    """Mostrar detalles de una casa específica"""
    casa = CasaService.obtener_por_id(id_casa)
    if not casa:
        return "Casa no encontrada", 404
    return render_template('detalle_casa.html', casa=casa)