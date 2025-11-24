from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.database import SessionLocal
from models.repositories import CasaRepository, LocacionRepository, AdminRepository, UsuarioRepository
from services.casa_service import CasaService
from services.locacion_service import LocacionService
from services.admin_service import AdminService
from services.usuario_service import UsuarioService

admin_bp = Blueprint('admin_bp', __name__)

# Helper para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        pass

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        admin = AdminService.verificar_credenciales(correo, contrasena)
        if admin:
            session['admin_id'] = admin['id_admin']
            session['admin_nombre'] = admin['nombre']
            return redirect(url_for('admin_bp.panel'))
        flash('Credenciales incorrectas', 'error')
    return render_template('login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin_bp.login'))

@admin_bp.route('/panel')
def panel():
    if 'admin_id' not in session:
        return redirect(url_for('admin_bp.login'))
    return render_template('admin_panel.html')

# ========== CRUD CASAS ==========

@admin_bp.route('/api/casas', methods=['GET'])
def get_casas():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    return jsonify(CasaService.obtener_todas(incluir_vendidas=True))

@admin_bp.route('/api/casas/<int:id>', methods=['GET'])
def get_casa(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    casa = CasaService.obtener_por_id(id)
    if casa and isinstance(casa.get('fotos'), list):
        casa['fotos'] = ', '.join(casa['fotos'])
    return jsonify(casa if casa else {})

@admin_bp.route('/api/casas', methods=['POST'])
def crear_casa():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    data = request.get_json()
    nueva = CasaService.crear(data)
    return jsonify({'success': True, 'data': nueva})

@admin_bp.route('/api/casas/<int:id>', methods=['PUT'])
def actualizar_casa(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    data = request.get_json()
    if 'fotos' in data and isinstance(data['fotos'], str):
        data['fotos'] = [f.strip() for f in data['fotos'].split(',') if f.strip()]
    actualizada = CasaService.actualizar(id, data)
    return jsonify({'success': True, 'data': actualizada})

@admin_bp.route('/api/casas/<int:id>', methods=['DELETE'])
def eliminar_casa(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    CasaService.eliminar(id)
    return jsonify({'success': True})

# ========== CRUD LOCACIONES ==========

@admin_bp.route('/api/locaciones', methods=['GET'])
def get_locaciones():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    return jsonify(LocacionService.obtener_todas())

@admin_bp.route('/api/locaciones/<int:id>', methods=['GET'])
def get_locacion(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    loc = LocacionService.obtener_por_id(id)
    return jsonify(loc if loc else {})

@admin_bp.route('/api/locaciones', methods=['POST'])
def crear_locacion():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    data = request.get_json()
    nueva = LocacionService.crear(data['nombre'])
    return jsonify({'success': True, 'data': nueva})

@admin_bp.route('/api/locaciones/<int:id>', methods=['PUT'])
def actualizar_locacion(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    data = request.get_json()
    act = LocacionService.actualizar(id, data['nombre'])
    return jsonify({'success': True, 'data': act})

@admin_bp.route('/api/locaciones/<int:id>', methods=['DELETE'])
def eliminar_locacion(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    LocacionService.eliminar(id)
    return jsonify({'success': True})

# ========== CRUD USUARIOS ==========

@admin_bp.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    return jsonify(UsuarioService.obtener_todos())

@admin_bp.route('/api/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    u = UsuarioService.obtener_por_id(id)
    return jsonify(u if u else {})

@admin_bp.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    data = request.get_json()
    nuevo = UsuarioService.crear(data)
    return jsonify({'success': True, 'data': nuevo})

@admin_bp.route('/api/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    data = request.get_json()
    actualizado = UsuarioService.actualizar(id, data)
    return jsonify({'success': True, 'data': actualizado})

@admin_bp.route('/api/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    UsuarioService.eliminar(id)
    return jsonify({'success': True})

# ========== DASHBOARD ==========

@admin_bp.route('/api/dashboard/estadisticas', methods=['GET'])
def get_estadisticas():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    stats = CasaService.obtener_estadisticas()
    todas = CasaService.obtener_todas(incluir_vendidas=True)
    rangos_costo = {'Menos de $1M': 0, '$1M - $2M': 0, '$2M - $3M': 0, 'Más de $3M': 0}
    for c in todas:
        costo = float(c['costo'])
        if costo < 1000000: rangos_costo['Menos de $1M'] += 1
        elif costo < 2000000: rangos_costo['$1M - $2M'] += 1
        elif costo < 3000000: rangos_costo['$2M - $3M'] += 1
        else: rangos_costo['Más de $3M'] += 1
    return jsonify({
        **stats,
        'rangos_costo': rangos_costo,
        'estatus': {'En Venta': stats['en_venta'], 'Vendida': stats['vendidas']}
    })