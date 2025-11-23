from flask import Blueprint, jsonify
from models.casa_model import Casa

mapa_bp = Blueprint('mapa_bp', __name__)

# --- Para usuarios: solo casas en venta ---
@mapa_bp.route('/casas/mapa', methods=['GET'])
def mapa_casas():
    casa = Casa()
    # Llamamos a un método que solo traiga casas en venta
    resultados = casa.obtener_para_mapa(solo_en_venta=True)
    return jsonify(resultados)

# --- Para admin: todas las casas ---
@mapa_bp.route('/admin/casas/mapa', methods=['GET'])
def mapa_casas_admin():
    casa = Casa()
    # Traemos todas las casas, sin filtrar por estatus
    resultados = casa.obtener_para_mapa(solo_en_venta=False)
    return jsonify(resultados)
