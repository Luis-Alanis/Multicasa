from flask import Blueprint, render_template, request, jsonify
from models.usuario_model import Usuario

contacto_bp = Blueprint('contacto_bp', __name__) 

usuario_model = Usuario()

@contacto_bp.route('/contactos', methods=['GET', 'POST'])
def contactos():
    if request.method == 'POST':
        print("POST RECIBIDO!")
        print(request.form)
        return "POST FUNCIONA"
    return render_template('contactos.html')


# ---- LISTAR TODOS ----
@contacto_bp.route('/contacto/listar', methods=['GET'])
def listar_contactos():
    contactos = usuario_model.obtener_todos()
    return jsonify(contactos)

# ---- VER UN CONTACTO POR ID ----
@contacto_bp.route('/contacto/ver/<int:id_usuario>', methods=['GET'])
def ver_contacto(id_usuario):
    contacto = usuario_model.obtener_por_id(id_usuario)
    if contacto:
        return jsonify(contacto)
    return jsonify({"error": "Contacto no encontrado"}), 404

@contacto_bp.route('/contacto/crear', methods=['POST'])
def crear_contacto():
    print(">>> SE EJECUTÓ crear_contacto <<<")
    # Recibir datos del formulario (POST normal)
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    telefono = request.form.get('telefono')
    asunto = request.form.get('asunto')
    mensaje = request.form.get('mensaje')
    estado = 'pendiente'

    # Validación
    if not nombre or not correo or not mensaje:
        return "Nombre, correo y mensaje son obligatorios", 400

    # Guardar en BD
    usuario_model.crear(nombre, correo, telefono, asunto, mensaje, estado)

    # Redirección o mensaje
    return "Contacto enviado correctamente"

# ---- ACTUALIZAR CONTACTO ----
@contacto_bp.route('/contacto/actualizar/<int:id_usuario>', methods=['PUT'])
def actualizar_contacto(id_usuario):
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    telefono = data.get('telefono')
    asunto = data.get('asunto')
    mensaje = data.get('mensaje')
    estado = data.get('estado')

    if not nombre or not correo or not mensaje:
        return jsonify({"error": "Nombre, correo y mensaje son obligatorios"}), 400

    updated = usuario_model.actualizar(id_usuario, nombre, correo, telefono, asunto, mensaje, estado)
    if updated:
        return jsonify({"success": "Contacto actualizado"})
    return jsonify({"error": "Contacto no encontrado"}), 404

# ---- ELIMINAR CONTACTO ----
@contacto_bp.route('/contacto/eliminar/<int:id_usuario>', methods=['DELETE'])
def eliminar_contacto(id_usuario):
    deleted = usuario_model.eliminar(id_usuario)
    if deleted:
        return jsonify({"success": "Contacto eliminado"})
    return jsonify({"error": "Contacto no encontrado"}), 404

# ---- BUSCAR CONTACTOS ----
@contacto_bp.route('/contacto/buscar', methods=['GET'])
def buscar_contacto():
    texto = request.args.get('q', '')
    resultados = usuario_model.buscar(texto)
    return jsonify(resultados)

