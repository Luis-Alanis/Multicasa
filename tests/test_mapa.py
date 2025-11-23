import webbrowser
from models.casa_model import Casa

# Instanciar el modelo y obtener las casas
casa_model = Casa()
#casas = casa_model.obtener_para_mapa()  #Casas en venta (usuario)
casas = casa_model.obtener_para_mapa(solo_en_venta=False) #Todas las casas (admin)


# Crear los marcadores en JS
marcadores_js = ""
for casa in casas:
    lat = casa.get("latitud")
    lon = casa.get("longitud")
    locacion = casa.get("locacion")
    costo = casa.get("costo")
    if lat and lon:
        marcadores_js += f"L.marker([{lat}, {lon}]).addTo(map).bindPopup('<b>{locacion}</b><br>Costo: ${costo}');\n"

# Generar el HTML completo
html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Mapa de Casas</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <style>
        #map {{ height: 600px; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([25.423, -100.952], 12); // Ajusta la vista inicial
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors'
        }}).addTo(map);

        {marcadores_js}
    </script>
</body>
</html>
"""

# Guardar el HTML
with open("mapa_casas.html", "w", encoding="utf-8") as f:
    f.write(html)

# Abrir automáticamente en el navegador por defecto
webbrowser.open("mapa_casas.html")
