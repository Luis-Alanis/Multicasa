document.addEventListener('DOMContentLoaded', function() {
    var mapEl = document.getElementById('mapa');
    if (!mapEl) return; // evita errores si no existe

    var map = L.map('mapa').setView([23.6345, -102.5528], 5);

    var resultadosEl = document.getElementById('resultados-data');
    var resultados = resultadosEl ? JSON.parse(resultadosEl.textContent) : [];

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    resultados.forEach(function(casa) {
        if(casa.latitud && casa.longitud) {
            var marker = L.marker([casa.latitud, casa.longitud]).addTo(map);
            var popupText = casa.locacion + ' - $' + casa.costo + ' - ' +
                            casa.recamaras + ' recámaras / ' +
                            casa.baños + ' baños';
            if(casa.distancia_km) popupText += ' - ' + casa.distancia_km.toFixed(2) + ' km';
            marker.bindPopup(popupText);
        }
    });

    if(resultados.length > 0) {
        var group = new L.featureGroup(resultados.map(c => L.marker([c.latitud, c.longitud])));
        map.fitBounds(group.getBounds().pad(0.2));
    }
});
