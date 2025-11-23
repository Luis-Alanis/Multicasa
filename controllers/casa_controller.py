from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.casa_model import Casa
from models.locacion_model import Locacion

bp = Blueprint('casas', __name__, url_prefix='/casas')

casa_model = Casa()
locacion_model = Locacion()

@bp.route('/')
def index():
    """Lista todas las casas"""
    casas = casa_model.obtener_todas()
    locaciones = locacion_model.obtener_todas()
    return render_template('crud/casas.html', casas=casas, locaciones=locaciones)

@bp.route('/crear', methods=['POST'])
def crear():
    """Crea una nueva casa"""
    try:
        casa_model.crear(
            id_locacion=request.form.get('id_locacion'),
            latitud=request.form.get('latitud'),
            longitud=request.form.get('longitud'),
            codigo_postal=request.form.get('codigo_postal'),
            costo=request.form.get('costo'),
            recamaras=request.form.get('recamaras'),
            banos=request.form.get('banos'),
            estatus_venta=request.form.get('estatus_venta'),
            fotos=request.form.get('fotos')
        )
        flash('Casa creada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al crear casa: {str(e)}', 'error')
    return redirect(url_for('casas.index'))

@bp.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    """Edita una casa existente"""
    try:
        casa_model.actualizar(
            id_casa=id,
            id_locacion=request.form.get('id_locacion'),
            latitud=request.form.get('latitud'),
            longitud=request.form.get('longitud'),
            codigo_postal=request.form.get('codigo_postal'),
            costo=request.form.get('costo'),
            recamaras=request.form.get('recamaras'),
            banos=request.form.get('banos'),
            estatus_venta=request.form.get('estatus_venta'),
            fotos=request.form.get('fotos')
        )
        flash('Casa actualizada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al actualizar casa: {str(e)}', 'error')
    return redirect(url_for('casas.index'))

@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    """Elimina una casa"""
    try:
        casa_model.eliminar(id)
        flash('Casa eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar casa: {str(e)}', 'error')
    return redirect(url_for('casas.index'))