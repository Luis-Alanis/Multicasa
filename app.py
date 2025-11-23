from flask import Flask, render_template, request, jsonify
from models.database import Database
from controllers import casa_controller, locacion_controller, usuario_controller
from controllers import admin_controller

app = Flask(__name__)
app.secret_key = ''

# Inicializar la base de datos
db = Database()

# Registrar blueprints
app.register_blueprint(admin_controller.bp)
app.register_blueprint(casa_controller.bp)
app.register_blueprint(locacion_controller.bp)
app.register_blueprint(usuario_controller.bp)

@app.route('/buscar')
def buscar():
    return render_template('search.html')

@app.route('/api/buscar-casas', methods=['GET'])
def buscar_casas():
    from models.casa_model import Casa
    casa_model = Casa()
    
    # Obtener parámetros de búsqueda
    ubicacion = request.args.get('ubicacion', '')
    precio_min = request.args.get('precioMin', type=float)
    precio_max = request.args.get('precioMax', type=float)
    recamaras = request.args.get('recamaras', type=int)
    banos = request.args.get('banos', type=int)
    
    # Buscar casas con los filtros
    casas = casa_model.buscar_avanzado(
        min_precio=precio_min,
        max_precio=precio_max,
        recamaras=recamaras,
        banos=banos
    )
    
    return jsonify(casas)

if __name__ == '__main__':
    app.run(debug=True)