/* ==========================================================================
   static/js/main.js - QUIOSCO DE ASISTENCIA CON REGISTRO DE ENTRADA Y SALIDA
   ========================================================================== */

function obtenerSerieTablet() {
    const claves = ["serie_dispositivo", "device_serial", "maquina_serie", "dev_id"];
    for (const k of claves) {
        const val = localStorage.getItem(k);
        if (val && val.startsWith("DEV-")) return val;
    }
    const hex = () => Math.random().toString(16).substring(2, 6).toUpperCase();
    const serie = `DEV-${hex()}-${hex()}-${hex()}-${hex()}`;
    localStorage.setItem("serie_dispositivo", serie);
    return serie;
}

function procesarMarcadoBiometrico() {
    const inputHuella = document.getElementById("huella");
    const mensajeSistema = document.getElementById("mensaje-sistema");
    const boxHuella = document.getElementById("contenedor-huella");
    const estadoLectura = document.getElementById("estado-lectura");
    const logHuella = document.getElementById("log-huella");
    const logDispositivo = document.getElementById("log-dispositivo");

    if (!boxHuella || boxHuella.classList.contains("capturada")) return;

    // 1. Captura del código biométrico al tocar el sensor
    // (Mientras conectas el SDK físico del sensor, toma el código de prueba registrado en tu BD)
    const huellaCapturada = "BIO_INDICE_dbovjyyne7"; 
    const serieTablet = obtenerSerieTablet();
    const lat = document.getElementById("latitud").value || "0";
    const lon = document.getElementById("longitud").value || "0";

    if (inputHuella) inputHuella.value = huellaCapturada;
    if (logHuella) logHuella.innerText = huellaCapturada;
    if (logDispositivo) logDispositivo.innerText = serieTablet;

    estadoLectura.innerHTML = "ESCANEANDO HUELLA Y VALIDANDO...";
    estadoLectura.style.color = "#1F4E78";
    if (mensajeSistema) mensajeSistema.classList.add("d-none");

    const formData = new FormData();
    formData.append("huella", huellaCapturada);
    formData.append("serie_dispositivo", serieTablet);
    formData.append("latitud", lat);
    formData.append("longitud", lon);

    fetch("/asistencia/api/registrar/", {
        method: "POST",
        body: formData
    })
    .then(async response => {
        const data = await response.json();
        if (!response.ok && response.status >= 500) {
            throw new Error(data.message || `Error HTTP: ${response.status}`);
        }
        return data;
    })
    .then(data => {
        if (mensajeSistema) mensajeSistema.classList.remove("d-none");

        if (data.status === "success") {
            // ENTRADA O SALIDA REGISTRADA CON ÉXITO
            boxHuella.classList.add("capturada");
            estadoLectura.innerHTML = "✓ MARCADO EXITOSO";
            estadoLectura.style.color = "#27AE60";
            mensajeSistema.className = "alert alert-success text-center font-weight-bold shadow-sm";
            mensajeSistema.innerHTML = `<i class="fas fa-check-circle"></i> ${data.message}`;

            setTimeout(() => restaurarPanelQuiosco(), 4500);

        } else if (data.status === "warning") {
            // YA TIENE ENTRADA Y SALIDA REGISTRADAS HOY
            boxHuella.classList.remove("capturada");
            estadoLectura.innerHTML = "⚠ JORNADA COMPLETA";
            estadoLectura.style.color = "#E67E22";
            mensajeSistema.className = "alert alert-warning text-center font-weight-bold shadow-sm";
            mensajeSistema.innerHTML = `<i class="fas fa-info-circle"></i> ${data.message}`;

            setTimeout(() => restaurarPanelQuiosco(), 4500);

        } else if (data.status === "invalid") {
            // RECHAZADO POR HUELLA, MÁQUINA O GPS (INCIDENCIA REGISTRADA)
            boxHuella.classList.remove("capturada");
            estadoLectura.innerHTML = "✖ ACCESO RECHAZADO";
            estadoLectura.style.color = "#E74C3C";
            mensajeSistema.className = "alert alert-danger text-center font-weight-bold shadow-sm";
            mensajeSistema.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${data.message}`;

            setTimeout(() => restaurarPanelQuiosco(), 5000);

        } else {
            boxHuella.classList.remove("capturada");
            estadoLectura.innerHTML = "⚠ ERROR DEL SISTEMA";
            estadoLectura.style.color = "#E74C3C";
            mensajeSistema.className = "alert alert-danger text-center font-weight-bold shadow-sm";
            mensajeSistema.innerHTML = `<i class="fas fa-times-circle"></i> ${data.message}`;

            setTimeout(() => restaurarPanelQuiosco(), 5000);
        }
    })
    .catch(error => {
        console.error("Error de comunicación:", error);
        estadoLectura.innerHTML = "✖ ERROR DE ENLACE DE RED";
        estadoLectura.style.color = "#E74C3C";
        if (mensajeSistema) {
            mensajeSistema.classList.remove("d-none");
            mensajeSistema.className = "alert alert-danger text-center font-weight-bold shadow-sm";
            mensajeSistema.innerHTML = `Error de conectividad con el servidor: ${error.message}`;
        }
        setTimeout(() => restaurarPanelQuiosco(), 5000);
    });
}

function restaurarPanelQuiosco() {
    const boxHuella = document.getElementById("contenedor-huella");
    const estadoLectura = document.getElementById("estado-lectura");
    const mensajeSistema = document.getElementById("mensaje-sistema");
    const inputHuella = document.getElementById("huella");
    const logHuella = document.getElementById("log-huella");

    if (boxHuella) boxHuella.classList.remove("capturada");
    if (estadoLectura) {
        estadoLectura.innerHTML = "TOQUE EL ESCÁNER PARA COLOCAR EL DEDO";
        estadoLectura.style.color = "#1F4E78";
    }
    if (mensajeSistema) mensajeSistema.className = "alert d-none";
    if (inputHuella) inputHuella.value = "";
    if (logHuella) logHuella.innerText = "Esperando lectura...";
}

document.addEventListener("DOMContentLoaded", function () {
    const logLatitud = document.getElementById("log-latitud");
    const logLongitud = document.getElementById("log-longitud");
    const logDispositivo = document.getElementById("log-dispositivo");

    if (logDispositivo) logDispositivo.innerText = obtenerSerieTablet();

    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(function (position) {
            const latFijada = position.coords.latitude.toFixed(6);
            const lonFijada = position.coords.longitude.toFixed(6);

            document.getElementById("latitud").value = latFijada;
            document.getElementById("longitud").value = lonFijada;
            if (logLatitud) logLatitud.innerText = latFijada;
            if (logLongitud) logLongitud.innerText = lonFijada;
        }, function () {
            if (logLatitud) logLatitud.innerText = "Sin señal GPS";
            if (logLongitud) logLongitud.innerText = "Sin señal GPS";
        }, {
            enableHighAccuracy: true,
            maximumAge: 0,
            timeout: 10000
        });
    }
});
