from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app
from flask_mail import Message
from models.usuario_model import Usuario
from datetime import datetime

contacto_bp = Blueprint('contacto_bp', __name__) 

usuario_model = Usuario()

@contacto_bp.route('/contactos', methods=['GET', 'POST'])
def contactos():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form.get('nombre')
            correo = request.form.get('correo')
            telefono = request.form.get('telefono', 'No proporcionado')
            asunto = request.form.get('asunto')
            mensaje = request.form.get('mensaje')
            
            # Validación
            if not nombre or not correo or not mensaje or not asunto:
                flash('Por favor completa todos los campos obligatorios', 'error')
                return redirect(url_for('contacto_bp.contactos'))
            
            # Guardar en la base de datos
            usuario_model.crear(nombre, correo, telefono, asunto, mensaje, estado='pendiente')
            
            # Enviar correo electrónico
            enviar_correo_contacto(nombre, correo, telefono, asunto, mensaje)
            
            flash('¡Mensaje enviado correctamente! Nos pondremos en contacto contigo pronto.', 'success')
            return redirect(url_for('contacto_bp.contactos'))
            
        except Exception as e:
            print(f"Error al procesar contacto: {str(e)}")
            flash('Hubo un error al enviar tu mensaje. Por favor intenta de nuevo.', 'error')
            return redirect(url_for('contacto_bp.contactos'))
    
    return render_template('contactos.html')

def enviar_correo_contacto(nombre, correo, telefono, asunto, mensaje):
    """Envía un correo electrónico cuando alguien llena el formulario de contacto"""
    try:
        mail = current_app.mail
        
        # Mapear asuntos a texto legible
        asuntos_dict = {
            'compra': 'Quiero comprar una propiedad',
            'venta': 'Quiero vender mi propiedad',
            'informacion': 'Solicitar información',
            'visita': 'Agendar una visita',
            'otro': 'Otro'
        }
        asunto_texto = asuntos_dict.get(asunto, asunto)
        
        # Crear mensaje para la empresa
        msg_empresa = Message(
            subject=f'Nuevo mensaje de contacto: {asunto_texto}',
            recipients=['multicasaserviciosbienesraices@gmail.com'],
            reply_to=correo
        )
        
        msg_empresa.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f9fc;
                }}
                .header {{
                    background: linear-gradient(to right, #1a5275, #134563);
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background: white;
                    padding: 30px;
                    border-radius: 0 0 5px 5px;
                }}
                .info-row {{
                    margin-bottom: 15px;
                    padding: 10px;
                    background: #f8f9fa;
                    border-left: 4px solid #2a9fd6;
                }}
                .label {{
                    font-weight: bold;
                    color: #134563;
                }}
                .mensaje {{
                    background: #fff;
                    border: 1px solid #d0dde6;
                    padding: 15px;
                    margin-top: 20px;
                    border-radius: 5px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    padding: 15px;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Nuevo Mensaje de Contacto</h2>
                    <p>Bienes Raíces MultiCasa</p>
                </div>
                <div class="content">
                    <p>Has recibido un nuevo mensaje de contacto desde el sitio web:</p>
                    
                    <div class="info-row">
                        <span class="label">Nombre:</span> {nombre}
                    </div>
                    
                    <div class="info-row">
                        <span class="label">Correo:</span> <a href="mailto:{correo}">{correo}</a>
                    </div>
                    
                    <div class="info-row">
                        <span class="label">Teléfono:</span> {telefono}
                    </div>
                    
                    <div class="info-row">
                        <span class="label">Asunto:</span> {asunto_texto}
                    </div>
                    
                    <div class="mensaje">
                        <p class="label">Mensaje:</p>
                        <p>{mensaje}</p>
                    </div>
                    
                    <div class="footer">
                        <p>Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                        <p>Este mensaje fue enviado desde el formulario de contacto de MultiCasa</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Crear mensaje de confirmación para el cliente
        msg_cliente = Message(
            subject='Confirmación de mensaje recibido - MultiCasa',
            recipients=[correo]
        )
        
        msg_cliente.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f9fc;
                }}
                .header {{
                    background: linear-gradient(to right, #1a5275, #134563);
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background: white;
                    padding: 30px;
                    border-radius: 0 0 5px 5px;
                }}
                .highlight {{
                    background: #e8f4f8;
                    padding: 15px;
                    border-left: 4px solid #2a9fd6;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    padding: 15px;
                    color: #666;
                    font-size: 12px;
                    border-top: 1px solid #d0dde6;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>¡Gracias por contactarnos!</h2>
                    <p>Bienes Raíces MultiCasa</p>
                </div>
                <div class="content">
                    <p>Hola <strong>{nombre}</strong>,</p>
                    
                    <p>Hemos recibido tu mensaje correctamente. Nuestro equipo revisará tu solicitud y se pondrá en contacto contigo lo antes posible.</p>
                    
                    <div class="highlight">
                        <p><strong>Resumen de tu mensaje:</strong></p>
                        <p><strong>Asunto:</strong> {asunto_texto}</p>
                        <p><strong>Mensaje:</strong> {mensaje[:100]}{'...' if len(mensaje) > 100 else ''}</p>
                    </div>
                    
                    <p>Si necesitas asistencia inmediata, puedes contactarnos por:</p>
                    <ul>
                        <li>📞 Teléfono: 1-800-123-4567</li>
                        <li>📧 Email: multicasaserviciosbienesraices@gmail.com</li>
                    </ul>
                    
                    <p>Horario de atención:<br>
                    Lunes a Viernes: 9:00 AM - 6:00 PM<br>
                    Sábados: 9:00 AM - 2:00 PM</p>
                    
                    <div class="footer">
                        <p><strong>Bienes Raíces MultiCasa</strong></p>
                        <p>Tu mejor opción en agencia de bienes raíces</p>
                        <p>© 2025 MultiCasa - Todos los derechos reservados</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Enviar ambos correos
        mail.send(msg_empresa)
        mail.send(msg_cliente)
        
        print(f"✅ Correos enviados correctamente a {correo}")
        
    except Exception as e:
        print(f"❌ Error al enviar correo: {str(e)}")
        raise

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
    # Esta ruta ya no se usa, todo se maneja en /contactos
    return redirect(url_for('contacto_bp.contactos'))

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

