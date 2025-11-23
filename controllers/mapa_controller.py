from flask import Blueprint, jsonify, request
from models.casa_model import Casa

mapa_bp = Blueprint('mapa_bp', __name__)

# --- Para usuarios: solo casas en venta ---
@mapa_bp.route('/casas/mapa', methods=['GET'])
def mapa_casas():
    # Parámetros del formulario (mismo que en buscar_casas)
    ubicacion = request.args.get('ubicacion')
    precio_min = request.args.get('precioMin', type=float)
    precio_max = request.args.get('precioMax', type=float)
    recamaras = request.args.get('recamaras')
    baños = request.args.get('baños')
    user_lat = request.args.get('user_lat', type=float)
    user_lon = request.args.get('user_lon', type=float)
    rango_km = request.args.get('rango_km', type=float)

    # Solo casas en venta para usuarios
    casa = Casa()
    resultados = casa.buscar_completo(
        ubicacion=ubicacion,
        precio_min=precio_min,
        precio_max=precio_max,
        recamaras=recamaras,
        baños=baños,
        user_lat=user_lat,
        user_lon=user_lon,
        rango_km=rango_km,
        incluir_vendidas=False
    )

    return jsonify(resultados)

# --- Para admin: todas las casas ---
@mapa_bp.route('/admin/casas/mapa', methods=['GET'])
def mapa_casas_admin():
    # Parámetros del formulario (mismo que en buscar_casas)
    ubicacion = request.args.get('ubicacion')
    precio_min = request.args.get('precioMin', type=float)
    precio_max = request.args.get('precioMax', type=float)
    recamaras = request.args.get('recamaras')
    baños = request.args.get('baños')
    user_lat = request.args.get('user_lat', type=float)
    user_lon = request.args.get('user_lon', type=float)
    rango_km = request.args.get('rango_km', type=float)

    # Solo casas en venta para usuarios
    casa = Casa()
    resultados = casa.buscar_completo(
        ubicacion=ubicacion,
        precio_min=precio_min,
        precio_max=precio_max,
        recamaras=recamaras,
        baños=baños,
        user_lat=user_lat,
        user_lon=user_lon,
        rango_km=rango_km,
        incluir_vendidas=True
    )

    return jsonify(resultados)
