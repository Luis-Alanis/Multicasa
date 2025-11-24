from flask import Blueprint, render_template, request, jsonify

menu_bp = Blueprint('menu_bp', __name__)

@menu_bp.route('/buscar')
def buscar():
    return render_template('search.html', resultados=[])

@menu_bp.route('/pago_extranjero')
def pago_extranjero():
    return render_template('pago_extranjero.html', resultados=[])

@menu_bp.route('/compania')
def compania():
    return render_template('compañia.html', resultados=[])

@menu_bp.route('/issste')
def issste():
    return render_template('issste.html', resultados=[])

@menu_bp.route('/eco_casa')
def eco_casa():
    return render_template('eco_casas.html', resultados=[])

@menu_bp.route('/iso_9001')
def iso_9001():
    return render_template('iso-9001.html', resultados=[])

@menu_bp.route('/politicas_calidad')
def politicas_calidad():
    return render_template('politicas_calidad.html', resultados=[])

@menu_bp.route('/tips')
def tips():
    return render_template('tips.html', resultados=[])

@menu_bp.route('/faq')
def faq():
    return render_template('faq.html', resultados=[])

@menu_bp.route('/requisitos')
def requisitos():
    return render_template('requisitos.html')

@menu_bp.route('/servicios')
def servicios():
    return render_template('servicios.html')