from flask import Flask, render_template
from controllers.casa_controller import casa_bp
from controllers.menu_controller import menu_bp
from controllers.admin_controller import admin_bp
from controllers.contacto_controller import contacto_bp

# Inicializar app
app = Flask(__name__)

# Registrar blueprint
app.register_blueprint(casa_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(contacto_bp)

# Ruta base
@app.route('/')
def index():
    return render_template('index.html')

# Correr app
if __name__ == "__main__":
    app.run(debug=True)
