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

            // Creamos contenido HTML para el popup con botón de Ver Detalles
            var popupContent = `
                <div style="text-align:center; max-width:220px;">
                    <img src="/static/images/casas/${primeraFoto}" 
                         alt="Casa" 
                         style="width:100%; height:auto; border-radius:5px; margin-bottom:8px;"
                         onerror="this.src='/static/images/no-image.jpg'">
                    <div style="font-weight:bold; font-size:14px; margin-bottom:5px; color:#134563;">
                        <i class="fas fa-map-marker-alt" style="color:#2a9fd6;"></i> ${casa.locacion}
                    </div>
                    <div style="font-size:16px; font-weight:bold; color:#2a9fd6; margin-bottom:5px;">
                        $${casa.costo.toLocaleString('es-MX', {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                    </div>
                    <div style="font-size:12px; color:#666; margin-bottom:8px;">
                        <i class="fas fa-bed" style="color:#2a9fd6;"></i> ${casa.recamaras} recámaras &nbsp;
                        <i class="fas fa-bath" style="color:#2a9fd6;"></i> ${casa.baños} baños
                        ${casa.distancia_km ? "- " + casa.distancia_km.toFixed(2) + " km" : ""}
                    </div>
                    <button onclick="window.location.href='/casas/detalles/${casa.id_casa}'" 
                            style="
                                width: 100%;
                                padding: 8px 12px;
                                background: linear-gradient(to bottom, #2a9fd6 0%, #1a8cc4 100%);
                                color: white;
                                border: none;
                                border-radius: 4px;
                                cursor: pointer;
                                font-weight: bold;
                                font-size: 13px;
                                transition: all 0.3s;
                            "
                            onmouseover="this.style.background='linear-gradient(to bottom, #1a8cc4 0%, #134563 100%)'"
                            onmouseout="this.style.background='linear-gradient(to bottom, #2a9fd6 0%, #1a8cc4 100%)'">
                        <i class="fas fa-arrow-right"></i> Ver Detalles
                    </button>
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
