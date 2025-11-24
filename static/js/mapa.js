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
        if (casa.latitud && casa.longitud) {
            const marker = L.marker([casa.latitud, casa.longitud]).addTo(map);

            // Obtener primera imagen segura
            let primeraFoto = null;
            if (Array.isArray(casa.fotos) && casa.fotos.length > 0) {
                primeraFoto = casa.fotos[0];
            } else if (casa.foto_principal) {
                primeraFoto = casa.foto_principal;
            }

            if (!primeraFoto) {
                primeraFoto = 'images/no-image.jpg';
            }

            // Normalizar ruta (asegurar prefijo /static/)
            const fotoUrl = primeraFoto.startsWith('/static/')
                ? primeraFoto
                : `/static/${primeraFoto.replace(/^\/+/, '')}`;

            const popupContent = `
                <div style="text-align:center;max-width:230px;">
                    <img src="${fotoUrl}"
                         alt="Casa en ${casa.locacion}"
                         style="width:100%;height:140px;object-fit:cover;border-radius:6px;margin-bottom:8px;"
                         onerror="this.src='/static/images/no-image.jpg'">
                    <div style="font-weight:bold;font-size:14px;margin-bottom:4px;color:#134563;">
                        <i class="fas fa-map-marker-alt" style="color:#2a9fd6;"></i> ${casa.locacion || 'Sin locación'}
                    </div>
                    <div style="font-size:16px;font-weight:bold;color:#2a9fd6;margin-bottom:6px;">
                        $${Number(casa.costo).toLocaleString('es-MX', {minimumFractionDigits:2, maximumFractionDigits:2})}
                    </div>
                    <div style="font-size:12px;color:#666;margin-bottom:8px;">
                        <i class="fas fa-bed" style="color:#2a9fd6;"></i> ${casa.recamaras} recámaras &nbsp;
                        <i class="fas fa-bath" style="color:#2a9fd6;"></i> ${casa.baños} baños
                        ${casa.distancia_km ? `<br><i class="fas fa-map-pin"></i> ${casa.distancia_km.toFixed(2)} km` : ''}
                    </div>
                    <button onclick="window.location.href='/casas/detalles/${casa.id_casa}'"
                        style="width:100%;padding:8px 12px;background:linear-gradient(to bottom,#2a9fd6,#1a8cc4);color:#fff;border:none;border-radius:5px;font-weight:bold;font-size:13px;cursor:pointer;">
                        Ver Detalles <i class="fas fa-arrow-right"></i>
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
