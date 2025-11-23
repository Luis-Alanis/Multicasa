document.addEventListener('DOMContentLoaded', function() {
    // Inicializamos el mapa centrado en México
    var map = L.map('mapa').setView([23.6345, -102.5528], 5);

    // Obtenemos resultados desde el script en HTML
    var resultadosEl = document.getElementById('resultados-data');
    var resultados = resultadosEl ? JSON.parse(resultadosEl.textContent) : [];

    // Agregamos el tile layer de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    resultados.forEach(function(casa) {
        if(casa.latitud && casa.longitud) {
            var marker = L.marker([casa.latitud, casa.longitud]).addTo(map);

            // Parseamos las fotos y usamos la primera
            var fotos = [];
            try {
                fotos = JSON.parse(casa.fotos || "[]");
            } catch(e) {
                console.error("Error al parsear fotos de la casa", casa.id_casa, e);
            }
            var primeraFoto = fotos.length > 0 ? fotos[0] : "placeholder.png";

            // Creamos contenido HTML para el popup
            var popupContent = `
                <div style="text-align:center; max-width:200px;">
                    <img src="/static/images/casas/${primeraFoto}" 
                         alt="Casa" 
                         style="width:100%; height:auto; border-radius:5px; margin-bottom:5px;">
                    <div style="font-weight:bold; font-size:14px; margin-bottom:3px;">
                        ${casa.locacion}
                    </div>
                    <div style="font-size:13px; margin-bottom:3px;">
                        $${casa.costo.toLocaleString()}
                    </div>
                    <div style="font-size:12px; color:#555;">
                        ${casa.recamaras} recámaras / ${casa.baños} baños
                        ${casa.distancia_km ? "- " + casa.distancia_km.toFixed(2) + " km" : ""}
                    </div>
                </div>
            `;

            marker.bindPopup(popupContent);
        }
    });

    // Ajustamos la vista para todos los marcadores
    if(resultados.length > 0) {
        var group = new L.featureGroup(resultados.map(c => L.marker([c.latitud, c.longitud])));
        map.fitBounds(group.getBounds().pad(0.2));
    }
});
