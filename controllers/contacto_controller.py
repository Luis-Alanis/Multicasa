from flask import Blueprint, render_template

contacto_bp = Blueprint('contacto_bp', __name__)

@contacto_bp.route('/contactos')
def contactos():
    return render_template('contactos.html')
