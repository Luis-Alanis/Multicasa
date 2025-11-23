from flask import Blueprint, request, jsonify
from models.casa_model import Casa

casa_bp = Blueprint('casa_bp', __name__)

@casa_bp.route('/casas/buscar', methods=['GET'])
def buscar_casas():

    ubicacion = request.args.get('ubicacion')
    precio_min = request.args.get('precioMin', type=float)
    precio_max = request.args.get('precioMax', type=float)
    recamaras = request.args.get('recamaras', type=int)
    baños = request.args.get('baños', type=int)

    user_lat = request.args.get('user_lat', type=float)
    user_lon = request.args.get('user_lon', type=float)
    rango_km = request.args.get('rango_km', type=float)

    casa = Casa()
    resultados = casa.buscar_completo(
        ubicacion=ubicacion,
        precio_min=precio_min,
        precio_max=precio_max,
        recamaras=recamaras,
        baños=baños,
        user_lat=user_lat,
        user_lon=user_lon,
        rango_km=rango_km
    )

    return jsonify(resultados)
