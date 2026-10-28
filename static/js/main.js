function procesarMarcadoBiometrico() {
    const inputHuella = document.getElementById("huella");
    const mensajeSistema = document.getElementById("mensaje-sistema");
    const boxHuella = document.getElementById("contenedor-huella");
    const estadoLectura = document.getElementById("estado-lectura");

    const logHuella = document.getElementById("log-huella");
    const logDispositivo = document.getElementById("log-dispositivo");

    if (!boxHuella || boxHuella.classList.contains("capturada")) return;

    estadoLectura.innerHTML = "⏳ ESCANEANDO CRESTAS PAPILARES...";
    if (mensajeSistema) mensajeSistema.classList.add("d-none");

    setTimeout(() => {
        // =========================================================================
        // BANCO DE VALORES CONFIGURABLES PARA PRUEBAS TÉCNICAS
        // =========================================================================
        
        // Huella 1 de tu Workbench: "BIO_INDICE_dbovjyyne7" 
        const huellaPrueba = "BIO_INDICE_dbovjyyne7"; 
        
        // Serie del hardware: Usa una que exista en tu tabla 'maquina' de Workbench
        const serieDispositivoPrueba = "MQ-YUNGAY-01"; 

        // =========================================================================

        if (inputHuella) inputHuella.value = huellaPrueba;
        if (logHuella) logHuella.innerText = huellaPrueba;
        if (logDispositivo) logDispositivo.innerText = serieDispositivoPrueba;

        const lat = document.getElementById("latitud").value || "-9.138472";
        const lon = document.getElementById("longitud").value || "-77.743911";

        const formData = new FormData();
        formData.append("huella", huellaPrueba);
        formData.append("latitud", lat);
        formData.append("longitud", lon);
        formData.append("serie_dispositivo", serieDispositivoPrueba);

        fetch("/asistencia/api/registrar/", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (mensajeSistema) mensajeSistema.classList.remove("d-none");

            if (data.status === "success") {
                // Éxito: Activa la animación del archivo recuadro_huella.css
                boxHuella.classList.add("capturada");
                estadoLectura.innerHTML = "✓ IDENTIDAD VERIFICADA";
                estadoLectura.style.color = "#27AE60";

                mensajeSistema.className = "alert alert-success text-center font-weight-bold shadow-sm";
                mensajeSistema.innerHTML = `<i class="fas fa-check-circle"></i> ${data.message}`;

                setTimeout(() => {
                    restaurarEstadoQuiosco(boxHuella, estadoLectura, mensajeSistema, inputHuella, logHuella);
                }, 4000);

            } else {
                // Denegado (Mala geolocalización o dispositivo inválido)
                boxHuella.classList.remove("capturada");
                estadoLectura.innerHTML = "❌ ACCESO RECHAZADO";
                estadoLectura.style.color = "#E74C3C";

                if (data.status === "invalid") {
                    mensajeSistema.className = "alert alert-warning text-center font-weight-bold shadow-sm";
                    mensajeSistema.innerHTML = `<i class="fas fa-exclamation-triangle"></i> RECHAZADO: ${data.message}`;
                } else {
                    mensajeSistema.className = "alert alert-danger text-center font-weight-bold shadow-sm";
                    mensajeSistema.innerHTML = `<i class="fas fa-times-circle"></i> ERROR: ${data.message}`;
                }

                setTimeout(() => {
                    restaurarEstadoQuiosco(boxHuella, estadoLectura, mensajeSistema, inputHuella, logHuella);
                }, 5000);
            }
        })
        .catch(error => {
            console.error("Fallo de canal de red:", error);
            estadoLectura.innerHTML = "❌ ERROR DE CONECTIVIDAD";
            estadoLectura.style.color = "#E74C3C";
            if (mensajeSistema) {
                mensajeSistema.classList.remove("d-none");
                mensajeSistema.className = "alert alert-danger text-center font-weight-bold shadow-sm";
                mensajeSistema.innerHTML = "⚠️ Canal de enlace inestable con la central de la UGEL.";
            }
        });

    }, 1200);
}

function restaurarEstadoQuiosco(box, estado, mensaje, inputH, logH) {
    if (box) box.classList.remove("capturada");
    if (estado) {
        estado.innerHTML = "TOQUE EL ESCÁNER PARA COLOCAR EL DEDO";
        estado.style.color = "#1F4E78";
    }
    if (mensaje) mensaje.classList.add("d-none");
    if (inputH) inputH.value = "";
    if (logH) logH.innerText = "Esperando lectura...";
}

// Inicializador de geolocalización de precisión por hardware
document.addEventListener("DOMContentLoaded", function () {
    const logLatitud = document.getElementById("log-latitud");
    const logLongitud = document.getElementById("log-longitud");
    const logDispositivo = document.getElementById("log-dispositivo");

    if (logDispositivo) logDispositivo.innerText = "SISTEMA-WEB-NAVEGADOR";

    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(function (position) {
            // Conversión matemática estricta a 6 decimales requerida por la base de datos
            const latFijada = position.coords.latitude.toFixed(6);
            const lonFijada = position.coords.longitude.toFixed(6);

            const latInput = document.getElementById("latitud");
            const lonInput = document.getElementById("longitud");
            
            if (latInput) latInput.value = latFijada;
            if (lonInput) lonInput.value = lonFijada;

            if (logLatitud) logLatitud.innerText = latFijada;
            if (logLongitud) logLongitud.innerText = lonFijada;
        }, function(error) {
            console.warn("Señal GPS degradada. Iniciando valores de respaldo.");
            const latRespaldo = "-9.138472";
            const lonRespaldo = "-77.743911";
            
            document.getElementById("latitud").value = latRespaldo;
            document.getElementById("longitud").value = lonRespaldo;

            if (logLatitud) logLatitud.innerText = latRespaldo + " (UGEL Simulado)";
            if (logLongitud) logLongitud.innerText = lonRespaldo + " (UGEL Simulado)";
        }, { 
            enableHighAccuracy: true,
            maximumAge: 0,
            timeout: 10000
        });
    }
});
