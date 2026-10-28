/* ==========================================================================
   static/js/main.js - LOGICA CENTRALIZADA DEL QUIOSCO DE ASISTENCIA
   ========================================================================== */

function procesarMarcadoBiometrico() {
    const inputHuella = document.getElementById("huella");
    const mensajeSistema = document.getElementById("mensaje-sistema");
    const boxHuella = document.getElementById("contenedor-huella");
    const estadoLectura = document.getElementById("estado-lectura");

    const logHuella = document.getElementById("log-huella");
    const logDispositivo = document.getElementById("log-dispositivo");

    // Evitar que se presione dos veces seguidas mientras se procesa la peticion
    if (!boxHuella || boxHuella.classList.contains("capturada")) return;

    // Animacion visual laser en el quiosco
    estadoLectura.innerHTML = "⏳ ESCANEANDO CRESTAS PAPILARES...";
    if (mensajeSistema) mensajeSistema.classList.add("d-none");

    setTimeout(() => {
        // =========================================================================
        // VALORES CONFIGURABLES PARA PRUEBAS (Empareja con tus datos de Workbench)
        // =========================================================================
        const huellaRealEmpleado = "BIO_INDICE_dbovjyyne7"; 
        const serieDispositivoReal = "MQ-YUNGAY-01"; 
        // =========================================================================

        if (inputHuella) inputHuella.value = huellaRealEmpleado;
        if (logHuella) logHuella.innerText = huellaRealEmpleado;
        if (logDispositivo) logDispositivo.innerText = serieDispositivoReal;

        const lat = document.getElementById("latitud").value || "-9.535284";
        const lon = document.getElementById("longitud").value || "-77.530053";

        // Empaquetar la trama de datos para la API
        const formData = new FormData();
        formData.append("huella", huellaRealEmpleado);
        formData.append("latitud", lat);
        formData.append("longitud", lon);
        formData.append("serie_dispositivo", serieDispositivoReal);

        // DIRECCION FISICA ABSOLUTA: Repara el error de enlace de red en dispositivos externos
        fetch("https://onrender.com", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (mensajeSistema) mensajeSistema.classList.remove("d-none");

            if (data.status === "success") {
                boxHuella.classList.add("capturada");
                estadoLectura.innerHTML = "✓ IDENTIDAD VERIFICADA";
                estadoLectura.style.color = "#27AE60";

                mensajeSistema.className = "alert alert-success text-center font-weight-bold shadow-sm";
                mensajeSistema.innerHTML = `<i class="fas fa-check-circle"></i> ${data.message}`;

                setTimeout(() => {
                    restaurarPanelQuiosco(boxHuella, estadoLectura, mensajeSistema, inputHuella, logHuella);
                }, 4000);

            } else if (data.status === "invalid") {
                boxHuella.classList.remove("capturada");
                estadoLectura.innerHTML = "❌ ACCESO RECHAZADO";
                estadoLectura.style.color = "#E74C3C";

                mensajeSistema.className = "alert alert-warning text-center font-weight-bold shadow-sm";
                mensajeSistema.innerHTML = `<i class="fas fa-exclamation-triangle"></i> RECHAZADO: ${data.message}`;

                setTimeout(() => {
                    restaurarPanelQuiosco(boxHuella, estadoLectura, mensajeSistema, inputHuella, logHuella);
                }, 5000);

            } else {
                boxHuella.classList.remove("capturada");
                estadoLectura.innerHTML = "⚠️ DETECCIÓN DE ERROR";
                estadoLectura.style.color = "#F1C40F";

                mensajeSistema.className = "alert alert-danger text-center font-weight-bold shadow-sm";
                mensajeSistema.innerHTML = `<i class="fas fa-times-circle"></i> DETALLES: ${data.message}`;

                setTimeout(() => {
                    restaurarPanelQuiosco(boxHuella, estadoLectura, mensajeSistema, inputHuella, logHuella);
                }, 5000);
            }
        })
        .catch(error => {
            console.error("Fallo de comunicación API:", error);
            estadoLectura.innerHTML = "❌ ERROR DE ENLACE DE RED";
            estadoLectura.style.color = "#E74C3C";
            if (mensajeSistema) {
                mensajeSistema.classList.remove("d-none");
                mensajeSistema.className = "alert alert-danger text-center font-weight-bold shadow-sm";
                mensajeSistema.innerHTML = "⚠️ Error crítico de conectividad con la central de la UGEL Yungay.";
            }
        });

    }, 1500);
}

function restaurarPanelQuiosco(box, estado, mensaje, inputH, logH) {
    if (box) box.classList.remove("capturada");
    if (estado) {
        estado.innerHTML = "TOQUE EL ESCÁNER PARA COLOCAR EL DEDO";
        estado.style.color = "#1F4E78";
    }
    if (mensaje) mensaje.className = "alert d-none";
    if (inputH) inputH.value = "";
    if (logH) logH.innerText = "Esperando lectura...";
}

document.addEventListener("DOMContentLoaded", function () {
    const logLatitud = document.getElementById("log-latitud");
    const logLongitud = document.getElementById("log-longitud");
    const logDispositivo = document.getElementById("log-dispositivo");

    if (logDispositivo) logDispositivo.innerText = "SISTEMA-WEB-NAVEGADOR";

    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(function (position) {
            const latFijada = position.coords.latitude.toFixed(6);
            const lonFijada = position.coords.longitude.toFixed(6);

            const latInput = document.getElementById("latitud");
            const lonInput = document.getElementById("longitud");
            
            if (latInput) latInput.value = latFijada;
            if (lonInput) lonInput.value = lonFijada;

            if (logLatitud) logLatitud.innerText = latFijada;
            if (logLongitud) logLongitud.innerText = lonFijada;
        }, function(error) {
            console.warn("Señal GPS baja. Aplicando respaldo.");
            const latRespaldo = "-9.535284";
            const lonRespaldo = "-77.530053";
            
            if (document.getElementById("latitud")) document.getElementById("latitud").value = latRespaldo;
            if (document.getElementById("longitud")) document.getElementById("longitud").value = lonRespaldo;

            if (logLatitud) logLatitud.innerText = latRespaldo;
            if (logLongitud) logLongitud.innerText = lonRespaldo;
        }, { 
            enableHighAccuracy: true,
            maximumAge: 0,
            timeout: 10000
        });
    }
});