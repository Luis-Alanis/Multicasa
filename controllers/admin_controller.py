from flask import Blueprint, json, render_template, request, redirect, url_for, session, flash, jsonify
from models.admin_model import Admin
from models.casa_model import Casa
from models.locacion_model import Locacion
from models.usuario_model import Usuario

admin_bp = Blueprint('admin_bp', __name__)

# Login
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        
        admin_model = Admin()
        admin = admin_model.obtener_por_correo(correo)
        
        if admin and admin['contraseña'] == contrasena:
            session['admin_id'] = admin['id_admin']
            session['admin_nombre'] = admin['nombre']
            return redirect(url_for('admin_bp.panel'))
        else:
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
    
    casa = Casa()
    casas = casa.obtener_todas()
    return jsonify(casas)

@admin_bp.route('/api/casas/<int:id>', methods=['GET'])
def get_casa(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    casa = Casa()
    result = casa.obtener_por_id(id)

    # Convertir JSON de fotos a string separado por comas
    if result and 'fotos' in result:
        try:
            fotos_list = json.loads(result['fotos'])
            result['fotos'] = ', '.join(fotos_list)
        except (json.JSONDecodeError, TypeError):
            result['fotos'] = ''

    return jsonify(result)

@admin_bp.route('/api/casas', methods=['POST'])
def crear_casa():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    data = request.get_json()
    casa = Casa()

    # Convertir fotos de string a lista JSON
    fotos_list = [f.strip() for f in data.get('fotos', '').split(',')] if data.get('fotos') else []

    casa.crear(
        data['id_locacion'],
        data['latitud'],
        data['longitud'],
        data.get('codigo_postal'),
        data['costo'],
        data['recamaras'],
        data['baños'],
        data['estatus_venta'],
        fotos_list
    )
    return jsonify({'success': True})

@admin_bp.route('/api/casas/<int:id>', methods=['PUT'])
def actualizar_casa(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    data = request.get_json()
    casa = Casa()

    # Convertir fotos de string a lista JSON
    fotos_list = [f.strip() for f in data.get('fotos', '').split(',')] if data.get('fotos') else []

    casa.actualizar(
        id,
        data['id_locacion'],
        data['latitud'],
        data['longitud'],
        data.get('codigo_postal'),
        data['costo'],
        data['recamaras'],
        data['baños'],
        data['estatus_venta'],
        fotos_list
    )
    return jsonify({'success': True})

@admin_bp.route('/api/casas/<int:id>', methods=['DELETE'])
def eliminar_casa(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    casa = Casa()
    casa.eliminar(id)
    return jsonify({'success': True})

# ========== CRUD LOCACIONES ==========

@admin_bp.route('/api/locaciones', methods=['GET'])
def get_locaciones():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    locacion = Locacion()
    locaciones = locacion.obtener_todas()
    return jsonify(locaciones)

@admin_bp.route('/api/locaciones/<int:id>', methods=['GET'])
def get_locacion(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    locacion = Locacion()
    result = locacion.obtener_por_id(id)
    return jsonify(result)

@admin_bp.route('/api/locaciones', methods=['POST'])
def crear_locacion():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    data = request.get_json()
    locacion = Locacion()
    locacion.crear(data['nombre'])
    return jsonify({'success': True})

@admin_bp.route('/api/locaciones/<int:id>', methods=['PUT'])
def actualizar_locacion(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    data = request.get_json()
    locacion = Locacion()
    locacion.actualizar(id, data['nombre'])
    return jsonify({'success': True})

@admin_bp.route('/api/locaciones/<int:id>', methods=['DELETE'])
def eliminar_locacion(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    locacion = Locacion()
    locacion.eliminar(id)
    return jsonify({'success': True})

# ========== CRUD USUARIOS ==========

@admin_bp.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    usuario = Usuario()
    usuarios = usuario.obtener_todos()
    return jsonify(usuarios)

@admin_bp.route('/api/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    usuario = Usuario()
    result = usuario.obtener_por_id(id)
    return jsonify(result)

@admin_bp.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    data = request.get_json()
    usuario = Usuario()
    usuario.crear(data['nombre'], data['correo'], data.get('telefono'))
    return jsonify({'success': True})

@admin_bp.route('/api/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    data = request.get_json()
    usuario = Usuario()
    usuario.actualizar(id, data['nombre'], data['correo'], data.get('telefono'))
    return jsonify({'success': True})

@admin_bp.route('/api/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    usuario = Usuario()
    usuario.eliminar(id)
    return jsonify({'success': True})

# ========== DASHBOARD ==========

@admin_bp.route('/api/dashboard/estadisticas', methods=['GET'])
def get_estadisticas():
    if 'admin_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    casa = Casa()
    todas_casas = casa.obtener_todas()
    
    # Estadísticas generales
    total_casas = len(todas_casas)
    en_venta = sum(1 for c in todas_casas if c['estatus_venta'] == 'En Venta')
    vendidas = sum(1 for c in todas_casas if c['estatus_venta'] == 'Vendida')
    
    # Calcular precio promedio
    if total_casas > 0:
        precio_promedio = sum(float(c['costo']) for c in todas_casas) / total_casas
    else:
        precio_promedio = 0
    
    # Agrupar por rangos de costo
    rangos_costo = {
        'Menos de $1M': 0,
        '$1M - $2M': 0,
        '$2M - $3M': 0,
        'Más de $3M': 0
    }
    
    for casa in todas_casas:
        costo = float(casa['costo'])
        if costo < 1000000:
            rangos_costo['Menos de $1M'] += 1
        elif costo < 2000000:
            rangos_costo['$1M - $2M'] += 1
        elif costo < 3000000:
            rangos_costo['$2M - $3M'] += 1
        else:
            rangos_costo['Más de $3M'] += 1
    
    return jsonify({
        'total_casas': total_casas,
        'en_venta': en_venta,
        'vendidas': vendidas,
        'precio_promedio': precio_promedio,
        'rangos_costo': rangos_costo,
        'estatus': {
            'En Venta': en_venta,
            'Vendida': vendidas
        }
    })