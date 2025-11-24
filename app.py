from flask import Flask, render_template
from flask_mail import Mail, Message
from controllers.casa_controller import casa_bp
from controllers.menu_controller import menu_bp
from controllers.admin_controller import admin_bp
from controllers.contacto_controller import contacto_bp
from controllers.reporte_casas_pdf_controller import reporte_bp
from controllers.ficha_tecnica_pdf_controller import ficha_bp
from controllers.mapa_controller import mapa_bp
import secrets

# Inicializar app
app = Flask(__name__)

app.secret_key = secrets.token_hex(32)

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'multicasaserviciosbienesraices@gmail.com'
app.config['MAIL_PASSWORD'] = 'tyyomeqxozsrxfds'
app.config['MAIL_DEFAULT_SENDER'] = 'multicasaserviciosbienesraices@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

# Inicializar Flask-Mail
mail = Mail(app)

# Hacer mail disponible globalmente
app.mail = mail

# Registrar blueprints
app.register_blueprint(casa_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(contacto_bp)
app.register_blueprint(reporte_bp)
app.register_blueprint(ficha_bp)
app.register_blueprint(mapa_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)