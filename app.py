from flask import Flask, render_template
from controllers.casa_controller import casa_bp
from controllers.menu_controller import menu_bp
from controllers.admin_controller import admin_bp
from controllers.contacto_controller import contacto_bp
from controllers.reporte_casas_pdf_controller import reporte_bp
import secrets

# Inicializar app
app = Flask(__name__)

app.secret_key = secrets.token_hex(32)

# Registrar blueprints
app.register_blueprint(casa_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(contacto_bp)
app.register_blueprint(reporte_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)