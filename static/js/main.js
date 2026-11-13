/* ==========================================================================
   static/js/main.js - LOGICA CENTRALIZADA DEL QUIOSCO DE ASISTENCIA
   ========================================================================== */

// 1. Obtener o generar la serie persistente de la tablet (DEV-XXXX-XXXX-XXXX-XXXX)
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

// 2. Activar lectura al tocar el recuadro del escáner en la tablet
function activarEscaneoTablet() {
    const inputHuella = document.getElementById("huella");
    const estadoLectura = document.getElementById("estado-lectura");
    if (inputHuella) {
        inputHuella.focus();
        if (estadoLectura) {
            estadoLectura.innerHTML = "ESCÁNER ACTIVO: APOYE EL DEDO...";
            estadoLectura.style.color = "#1F4E78";
        }
    }
}

// 3. Procesar envío a Django
function procesarMarcadoBiometrico() {
    const inputHuella = document.getElementById("huella");
    const mensajeSistema = document.getElementById("mensaje-sistema");
    const boxHuella = document.getElementById("contenedor-huella");
    const estadoLectura = document.getElementById("estado-lectura");
    const logHuella = document.getElementById("log-huella");
    const logDispositivo = document.getElementById("log-dispositivo");

    if (!boxHuella || boxHuella.classList.contains("capturada")) return;

    const codigoHuella = inputHuella ? inputHuella.value.trim() : "";
    if (!codigoHuella) {
        activarEscaneoTablet();
        return;
    }

    const serieTablet = obtenerSerieTablet();
    const lat = document.getElementById("latitud").value || "0";
    const lon = document.getElementById("longitud").value || "0";

    if (logHuella) logHuella.innerText = codigoHuella;
    if (logDispositivo) logDispositivo.innerText = serieTablet;

    estadoLectura.innerHTML = "VALIDANDO EN SERVIDOR UGEL...";
    if (mensajeSistema) mensajeSistema.classList.add("d-none");

    const formData = new FormData();
    formData.append("huella", codigoHuella);
    formData.append("serie_dispositivo", serieTablet);
    formData.append("latitud", lat);
    formData.append("longitud", lon);

    // URL exacta definida en asistencia/urls.py
    fetch("/asistencia/api/registrar/", {
        method: "POST",
        body: formData
    })
    .then(async response => {
        const data = await response.json();
        if (!response.ok && response.status >= 500) {
            throw new Error(data.message || `HTTP Error: ${response.status}`);
        }
        return data;
    })
    .then(data => {
        if (mensajeSistema) mensajeSistema.classList.remove("d-none");

        if (data.status === "success") {
            boxHuella.classList.add("capturada");
            estadoLectura.innerHTML = "✓ IDENTIDAD VERIFICADA";
            estadoLectura.style.color = "#27AE60";
            mensajeSistema.className = "alert alert-success text-center font-weight-bold shadow-sm";
            mensajeSistema.innerHTML = `<i class="fas fa-check-circle"></i> ${data.message}`;

            setTimeout(() => restaurarPanelQuiosco(), 4000);

        } else if (data.status === "invalid") {
            boxHuella.classList.remove("capturada");
            estadoLectura.innerHTML = "✖ ACCESO RECHAZADO";
            estadoLectura.style.color = "#E74C3C";
            mensajeSistema.className = "alert alert-warning text-center font-weight-bold shadow-sm";
            mensajeSistema.innerHTML = `<i class="fas fa-exclamation-triangle"></i> RECHAZADO: ${data.message}`;

            setTimeout(() => restaurarPanelQuiosco(), 5000);

        } else {
            boxHuella.classList.remove("capturada");
            estadoLectura.innerHTML = "⚠ AVISO DEL SISTEMA";
            estadoLectura.style.color = "#F1C40F";
            mensajeSistema.className = "alert alert-danger text-center font-weight-bold shadow-sm";
            mensajeSistema.innerHTML = `<i class="fas fa-times-circle"></i> ${data.message}`;

            setTimeout(() => restaurarPanelQuiosco(), 5000);
        }
    })
    .catch(error => {
        console.error("Fallo de comunicación API:", error);
        estadoLectura.innerHTML = "✖ ERROR DE ENLACE DE RED";
        estadoLectura.style.color = "#E74C3C";
        if (mensajeSistema) {
            mensajeSistema.classList.remove("d-none");
            mensajeSistema.className = "alert alert-danger text-center font-weight-bold shadow-sm";
            mensajeSistema.innerHTML = `Error crítico de conectividad con la central de la UGEL Yungay: ${error.message}`;
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
    if (inputHuella) {
        inputHuella.value = "";
        inputHuella.focus();
    }
    if (logHuella) logHuella.innerText = "Esperando lectura...";
}

// 4. Inicialización de GPS y serie de dispositivo al abrir el quiosco
document.addEventListener("DOMContentLoaded", function () {
    const logLatitud = document.getElementById("log-latitud");
    const logLongitud = document.getElementById("log-longitud");
    const logDispositivo = document.getElementById("log-dispositivo");
    const inputHuella = document.getElementById("huella");

    if (logDispositivo) logDispositivo.innerText = obtenerSerieTablet();
    if (inputHuella) inputHuella.focus();

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
        }, function (error) {
            console.warn("Error GPS:", error);
            if (logLatitud) logLatitud.innerText = "Error GPS - Active ubicación";
            if (logLongitud) logLongitud.innerText = "Error GPS - Active ubicación";
        }, {
            enableHighAccuracy: true,
            maximumAge: 0,
            timeout: 10000
        });
    }
});
