document.addEventListener("DOMContentLoaded", () => {

    const btnBuscar = document.getElementById("btnBuscar");
    const form = document.querySelector(".search-box.search-page");

    btnBuscar.addEventListener("click", () => {

        const rango = form.querySelector('select[name="rango_km"]').value;

        // Si no seleccionó rango → búsqueda sin geolocalizar
        if (rango === "") {
            form.submit();
            return;
        }

        // Si sí seleccionó rango → pedir ubicación
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    document.getElementById("user_lat").value = pos.coords.latitude;
                    document.getElementById("user_lon").value = pos.coords.longitude;

                    form.submit();
                },
                () => {
                    alert("No se pudo obtener tu ubicación, pero la búsqueda continuará sin distancia.");
                    form.submit();
                }
            );
        } else {
            alert("Tu navegador no soporta geolocalización.");
            form.submit();
        }
    });
});