function procesarMarcadoBiometrico() {
    const inputHuella = document.getElementById("huella");
    const mensajeSistema = document.getElementById("mensaje-sistema");
    const boxHuella = document.getElementById("contenedor-huella");
    const estadoLectura = document.getElementById("estado-lectura");

    // Elementos de la consola de diagnóstico
    const logHuella = document.getElementById("log-huella");

    if (!boxHuella || boxHuella.classList.contains("capturada")) return;

    estadoLectura.innerHTML = "⏳ PROCESANDO HUELLA...";
    if (mensajeSistema) mensajeSistema.classList.add("d-none");

    setTimeout(() => {
        // Clonamos tu formato de hash nativo de la tabla Personal
        const tokenHuella = "BIO_INDICE_" + Math.random().toString(36).substring(2, 12).toUpperCase();
        if (inputHuella) inputHuella.value = tokenHuella;

        // Imprimir token de huella generado en la consola de diagnóstico
        if (logHuella) logHuella.innerText = tokenHuella;

        const lat = document.getElementById("latitud").value || "-9.530000";
        const lon = document.getElementById("longitud").value || "-77.530000";

        const formData = new FormData();
        formData.append("huella", tokenHuella);
        formData.append("latitud", lat);
        formData.append("longitud", lon);
        formData.append("serie_dispositivo", "PC-LOCAL-NAVEGADOR");

        fetch("/asistencia/api/registrar/", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (mensajeSistema) mensajeSistema.classList.remove("d-none");

            if (data.status === "success") {
                boxHuella.classList.add("capturada");
                estadoLectura.innerHTML = "✓ IDENTIDAD VERIFICADA";
                estadoLectura.style.color = "#27AE60";

                mensajeSistema.className = "alert alert-success text-center font-weight-bold shadow-sm";
                mensajeSistema.innerHTML = `<i class="fas fa-check-circle"></i> ${data.message}`;

                setTimeout(() => {
                    boxHuella.classList.remove("capturada");
                    estadoLectura.innerHTML = "TOQUE EL ESCÁNER PARA COLOCAR EL DEDO";
                    estadoLectura.style.color = "#1F4E78";
                    mensajeSistema.classList.add("d-none");
                    if (inputHuella) inputHuella.value = "";
                    if (logHuella) logHuella.innerText = "Esperando lectura...";
                }, 3500);

            } else {
                boxHuella.classList.remove("capturada");
                estadoLectura.innerHTML = "❌ ACCESO DENEGADO";
                estadoLectura.style.color = "#E74C3C";

                mensajeSistema.className = "alert alert-danger text-center font-weight-bold shadow-sm";
                mensajeSistema.innerHTML = `<i class="fas fa-times-circle"></i> ${data.message}`;

                setTimeout(() => {
                    estadoLectura.innerHTML = "TOQUE EL ESCÁNER PARA COLOCAR EL DEDO";
                    estadoLectura.style.color = "#1F4E78";
                    mensajeSistema.classList.add("d-none");
                    if (inputHuella) inputHuella.value = "";
                    if (logHuella) logHuella.innerText = "Esperando lectura...";
                }, 4000);
            }
        })
        .catch(error => {
            estadoLectura.innerHTML = "TOQUE EL ESCÁNER PARA COLOCAR EL DEDO";
            if (mensajeSistema) {
                mensajeSistema.classList.remove("d-none");
                mensajeSistema.className = "alert alert-danger text-center font-weight-bold";
                mensajeSistema.innerHTML = "⚠️ Error de comunicación con el servidor.";
            }
        });

    }, 1500);
}

document.addEventListener("DOMContentLoaded", function () {
    const logLatitud = document.getElementById("log-latitud");
    const logLongitud = document.getElementById("log-longitud");

    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(function (position) {
            // Aseguramos que se guarden y muestren con signo negativo y exactamente 6 decimales
            const latFijada = position.coords.latitude.toFixed(6);
            const lonFijada = position.coords.longitude.toFixed(6);

            const latInput = document.getElementById("latitud");
            const lonInput = document.getElementById("longitud");
            
            if (latInput) latInput.value = latFijada;
            if (lonInput) lonInput.value = lonFijada;

            // Imprimir de inmediato en el panel visual gris
            if (logLatitud) logLatitud.innerText = latFijada;
            if (logLongitud) logLongitud.innerText = lonFijada;
        }, function(error) {
            if (logLatitud) logLatitud.innerText = "-9.530000 (Simulado)";
            if (logLongitud) logLongitud.innerText = "-77.530000 (Simulado)";
        }, { enableHighAccuracy: true });
    }
});
