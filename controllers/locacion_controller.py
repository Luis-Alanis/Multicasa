from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.locacion_model import Locacion

bp = Blueprint('locaciones', __name__, url_prefix='/locaciones')

locacion_model = Locacion()

@bp.route('/')
def index():
    """Lista todas las locaciones"""
    locaciones = locacion_model.obtener_todas()
    return render_template('crud/locaciones.html', locaciones=locaciones)

@bp.route('/crear', methods=['POST'])
def crear():
    """Crea una nueva locación"""
    try:
        locacion_model.crear(nombre=request.form.get('nombre'))
        flash('Locación creada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al crear locación: {str(e)}', 'error')
    return redirect(url_for('locaciones.index'))

@bp.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    """Edita una locación existente"""
    try:
        locacion_model.actualizar(
            id_locacion=id,
            nombre=request.form.get('nombre')
        )
        flash('Locación actualizada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al actualizar locación: {str(e)}', 'error')
    return redirect(url_for('locaciones.index'))

@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    """Elimina una locación"""
    try:
        locacion_model.eliminar(id)
        flash('Locación eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar locación: {str(e)}', 'error')
    return redirect(url_for('locaciones.index'))