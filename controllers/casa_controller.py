from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from models.casa_model import Casa
import json

casa_bp = Blueprint('casa_bp', __name__)

@casa_bp.route('/casas/buscar', methods=['GET'])
def buscar_casas():

    ubicacion = request.args.get('ubicacion')
    precio_min = request.args.get('precioMin', type=float)
    precio_max = request.args.get('precioMax', type=float)
    recamaras = request.args.get('recamaras')
    baños = request.args.get('baños')
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

    # Procesar fotos para cada resultado
    for resultado in resultados:
        if resultado.get('fotos'):
            try:
                # Intentar parsear como JSON
                fotos = json.loads(resultado['fotos'])
                if isinstance(fotos, list) and len(fotos) > 0:
                    # Asegurarse de que las rutas sean correctas
                    resultado['fotos_lista'] = [f"images/casas/{foto}" if not foto.startswith('images/') else foto for foto in fotos]
                    resultado['foto_principal'] = resultado['fotos_lista'][0]
                else:
                    resultado['fotos_lista'] = []
                    resultado['foto_principal'] = 'images/no-image.jpg'
            except json.JSONDecodeError:
                # Si falla el JSON, intentar separar por comas
                fotos_raw = [foto.strip() for foto in resultado['fotos'].split(',') if foto.strip()]
                if fotos_raw:
                    resultado['fotos_lista'] = [f"images/casas/{foto}" if not foto.startswith('images/') else foto for foto in fotos_raw]
                    resultado['foto_principal'] = resultado['fotos_lista'][0]
                else:
                    resultado['fotos_lista'] = []
                    resultado['foto_principal'] = 'images/no-image.jpg'
        else:
            resultado['fotos_lista'] = []
            resultado['foto_principal'] = 'images/no-image.jpg'

    return render_template('search.html',
        resultados=resultados,
        ubicacion=ubicacion or "",
        precio_min=precio_min or "",
        precio_max=precio_max or "",
        recamaras=recamaras or "",
        baños=baños or "",
        rango_km=rango_km or ""
    )

@casa_bp.route('/casas/detalles/<int:id_casa>', methods=['GET'])
def detalles_casa(id_casa):
    casa = Casa()
    resultado = casa.obtener_por_id(id_casa)
    
    if not resultado:
        flash('Casa no encontrada', 'error')
        return redirect(url_for('menu_bp.buscar'))
    
    # Procesar fotos
    if resultado.get('fotos'):
        try:
            fotos = json.loads(resultado['fotos'])
            if isinstance(fotos, list) and len(fotos) > 0:
                resultado['fotos_lista'] = [f"images/casas/{foto}" if not foto.startswith('images/') else foto for foto in fotos]
            else:
                resultado['fotos_lista'] = ['images/no-image.jpg']
        except json.JSONDecodeError:
            fotos_raw = [foto.strip() for foto in resultado['fotos'].split(',') if foto.strip()]
            if fotos_raw:
                resultado['fotos_lista'] = [f"images/casas/{foto}" if not foto.startswith('images/') else foto for foto in fotos_raw]
            else:
                resultado['fotos_lista'] = ['images/no-image.jpg']
    else:
        resultado['fotos_lista'] = ['images/no-image.jpg']
    
    return render_template('detalle_casa.html', casa=resultado)