from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.usuario_model import Usuario

bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

usuario_model = Usuario()

@bp.route('/')
def index():
    """Lista todos los usuarios"""
    usuarios = usuario_model.obtener_todos()
    return render_template('crud/usuarios.html', usuarios=usuarios)

@bp.route('/crear', methods=['POST'])
def crear():
    """Crea un nuevo usuario"""
    try:
        usuario_model.crear(
            nombre=request.form.get('nombre'),
            correo=request.form.get('correo'),
            telefono=request.form.get('telefono')
        )
        flash('Usuario creado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al crear usuario: {str(e)}', 'error')
    return redirect(url_for('usuarios.index'))

@bp.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    """Edita un usuario existente"""
    try:
        usuario_model.actualizar(
            id_usuario=id,
            nombre=request.form.get('nombre'),
            correo=request.form.get('correo'),
            telefono=request.form.get('telefono')
        )
        flash('Usuario actualizado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al actualizar usuario: {str(e)}', 'error')
    return redirect(url_for('usuarios.index'))

@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    """Elimina un usuario"""
    try:
        usuario_model.eliminar(id)
        flash('Usuario eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar usuario: {str(e)}', 'error')
    return redirect(url_for('usuarios.index'))