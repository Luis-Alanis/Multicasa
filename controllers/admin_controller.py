from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.admin_model import Admin
from models.casa_model import Casa
from models.locacion_model import Locacion
from models.usuario_model import Usuario
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

admin_model = Admin()
casa_model = Casa()
locacion_model = Locacion()
usuario_model = Usuario()

# Decorador para proteger rutas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Debes iniciar sesión para acceder', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        
        # Buscar admin por correo
        admin = admin_model.obtener_por_correo(correo)
        
        if admin and admin['contraseña'] == contrasena:
            session['admin_id'] = admin['id_admin']
            session['admin_nombre'] = admin['nombre']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Correo o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('admin.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal del admin con todos los datos"""
    casas = casa_model.obtener_todas()
    locaciones = locacion_model.obtener_todas()
    usuarios = usuario_model.obtener_todos()
    
    return render_template('admin/dashboard.html', 
                         casas=casas, 
                         locaciones=locaciones, 
                         usuarios=usuarios)

# ========== RUTAS PARA CASAS ==========

@bp.route('/casas/crear', methods=['POST'])
@login_required
def crear_casa():
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
            fotos=request.form.get('fotos', '')
        )
        flash('Casa creada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al crear casa: {str(e)}', 'error')
    return redirect(url_for('admin.dashboard'))

@bp.route('/casas/editar/<int:id>', methods=['POST'])
@login_required
def editar_casa(id):
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
            fotos=request.form.get('fotos', '')
        )
        flash('Casa actualizada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al actualizar casa: {str(e)}', 'error')
    return redirect(url_for('admin.dashboard'))

@bp.route('/casas/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_casa(id):
    """Elimina una casa"""
    try:
        casa_model.eliminar(id)
        flash('Casa eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar casa: {str(e)}', 'error')
    return redirect(url_for('admin.dashboard'))

# ========== RUTAS PARA LOCACIONES ==========

@bp.route('/locaciones/crear', methods=['POST'])
@login_required
def crear_locacion():
    """Crea una nueva locación"""
    try:
        locacion_model.crear(nombre=request.form.get('nombre'))
        flash('Locación creada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al crear locación: {str(e)}', 'error')
    return redirect(url_for('admin.dashboard'))

@bp.route('/locaciones/editar/<int:id>', methods=['POST'])
@login_required
def editar_locacion(id):
    """Edita una locación existente"""
    try:
        locacion_model.actualizar(
            id_locacion=id,
            nombre=request.form.get('nombre')
        )
        flash('Locación actualizada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al actualizar locación: {str(e)}', 'error')
    return redirect(url_for('admin.dashboard'))

@bp.route('/locaciones/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_locacion(id):
    """Elimina una locación"""
    try:
        locacion_model.eliminar(id)
        flash('Locación eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar locación: {str(e)}', 'error')
    return redirect(url_for('admin.dashboard'))

# ========== RUTAS PARA USUARIOS ==========

@bp.route('/usuarios/crear', methods=['POST'])
@login_required
def crear_usuario():
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
    return redirect(url_for('admin.dashboard'))

@bp.route('/usuarios/editar/<int:id>', methods=['POST'])
@login_required
def editar_usuario(id):
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
    return redirect(url_for('admin.dashboard'))

@bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    """Elimina un usuario"""
    try:
        usuario_model.eliminar(id)
        flash('Usuario eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar usuario: {str(e)}', 'error')
    return redirect(url_for('admin.dashboard'))