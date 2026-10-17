// Función global que se activa al interactuar con el escáner láser
function procesarMarcadoBiometrico() {
    const inputHuella = document.getElementById("huella");
    const mensajeSistema = document.getElementById("mensaje-sistema");
    const boxHuella = document.getElementById("contenedor-huella");
    const estadoLectura = document.getElementById("estado-lectura");

    if (!boxHuella || boxHuella.classList.contains("capturada")) return;

    // 1. Clonamos la lógica de simulación de tu archivo Personal
    estadoLectura.innerHTML = "⏳ PROCESANDO HUELLA...";
    if (mensajeSistema) mensajeSistema.classList.add("d-none");

    // Simulamos un retraso de lectura idéntico al de tu registro (1.5 segundos)
    setTimeout(() => {
        // Genera un token aleatorio emulando el comportamiento de tu modulo Personal
        const tokenHuella = "BIO_INDICE_" + Math.random().toString(36).substring(2, 12).toUpperCase();
        if (inputHuella) inputHuella.value = tokenHuella;

        const lat = document.getElementById("latitud").value || "-9.53000000";
        const lon = document.getElementById("longitud").value || "-77.53000000";

        // Preparación del paquete de envío hacia Django
        const formData = new FormData();
        formData.append("huella", tokenHuella);
        formData.append("latitud", lat);
        formData.append("longitud", lon);
        formData.append("serie_dispositivo", "PC-LOCAL-NAVEGADOR");

        // Realizar la búsqueda y validación en cascada en el servidor
        fetch("/asistencia/api/registrar/", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (mensajeSistema) mensajeSistema.classList.remove("d-none");

            if (data.status === "success") {
                // --- CASO: PERSONAL VÁLIDO / REGISTRO CORRECTO ---
                boxHuella.classList.add("capturada");
                estadoLectura.innerHTML = "✓ IDENTIDAD VERIFICADA";
                estadoLectura.style.color = "#27AE60";

                mensajeSistema.className = "alert alert-success text-center font-weight-bold shadow-sm";
                mensajeSistema.innerHTML = `<i class="fas fa-check-circle"></i> ${data.message}`;

                // Temporizador de reseteo para el siguiente trabajador
                setTimeout(() => {
                    boxHuella.classList.remove("capturada");
                    estadoLectura.innerHTML = "TOQUE EL ESCÁNER PARA COLOCAR EL DEDO";
                    estadoLectura.style.color = "#1F4E78";
                    mensajeSistema.classList.add("d-none");
                    if (inputHuella) inputHuella.value = "";
                }, 3500);

            } else {
                // --- CASO: EL USUARIO NO EXISTE O INCIDENCIA ---
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

// Invocación pasiva de geolocalización al cargar la página
document.addEventListener("DOMContentLoaded", function () {
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(function (position) {
            const latInput = document.getElementById("latitud");
            const lonInput = document.getElementById("longitud");
            if (latInput) latInput.value = position.coords.latitude;
            if (lonInput) lonInput.value = position.coords.longitude;
        }, null, { enableHighAccuracy: true });
    }
});
