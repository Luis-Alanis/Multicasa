from flask import Flask, render_template
from controllers.casa_controller import casa_bp

# Inicializar app
app = Flask(__name__)

# Registrar blueprint
app.register_blueprint(casa_bp)

# Ruta base opcional
@app.route('/')
def index():
    return render_template('index.html')

# Correr app
if __name__ == "__main__":
    app.run(debug=True)
