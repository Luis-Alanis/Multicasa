from flask import Blueprint, render_template, request, jsonify

menu_bp = Blueprint('menu_bp', __name__)

@menu_bp.route('/buscar')
def buscar():
    return render_template('search.html')