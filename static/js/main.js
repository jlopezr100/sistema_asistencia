// Mantener el foco automático en el campo del lector para marcados rápidos
const inputHuella = document.getElementById("huella");
if (inputHuella) {
    inputHuella.focus();
    // Si el usuario hace clic afuera, reenfocar automáticamente a los 2 segundos
    document.addEventListener("click", () => {
        setTimeout(() => { inputHuella.focus(); }, 2000);
    });
}
document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const btnMarcar = document.getElementById("btn-marcar");
    const mensajeSistema = document.getElementById("mensaje-sistema");

    // 1. Activar la Cámara Web automáticamente al cargar la pantalla
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
            })
            .catch(function (error) {
                mostrarMensaje("Error al acceder a la cámara web. Verifica los permisos.", "alert-danger");
            });
    }

    // 2. Capturar las coordenadas de Geolocalización (GPS) en tiempo real
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(function (position) {
            document.getElementById("latitud").value = position.coords.latitude;
            document.getElementById("longitud").value = position.coords.longitude;
        }, function (error) {
            mostrarMensaje("Por favor, activa la ubicación GPS en tu dispositivo para poder marcar.", "alert-warning");
        }, { enableHighAccuracy: true });
    } else {
        mostrarMensaje("Tu navegador no soporta geolocalización.", "alert-danger");
    }

    // 3. Evento al hacer clic en el botón de Marcar
    btnMarcar.addEventListener("click", function () {
        const huella = document.getElementById("huella").value;
        const lat = document.getElementById("latitud").value;
        const lon = document.getElementById("longitud").value;

        if (!huella) {
            mostrarMensaje("Debe ingresar o escanear una huella digital.", "alert-warning");
            return;
        }
        if (!lat || !lon) {
            mostrarMensaje("Esperando señal GPS válida... Intente de nuevo en unos segundos.", "alert-warning");
            return;
        }

        // Bloquear botón temporalmente
        btnMarcar.disabled = true;

        // Capturar el fotograma actual de la cámara web
        const context = canvas.getContext("2d");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);

        // Convertir la captura del canvas a un archivo BLOB (binario) de tipo imagen
        canvas.toBlob(function (blob) {
            const formData = new FormData();
            formData.append("huella", huella);
            formData.append("latitud", lat);
            formData.append("longitud", lon);
            formData.append("serie_dispositivo", "PC-LOCAL-NAVEGADOR"); // Reemplazar dinámicamente si se expone la serie del cliente
            formData.append("ubicacion_imagen", blob, `marcado_${Date.now()}.jpg`);

            // Enviar la información completa a Django mediante AJAX Fetch
            // Enviar la información completa a Django mediante AJAX Fetch
            fetch("/asistencia/api/registrar/", {
                method: "POST",
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    btnMarcar.disabled = false;
                    const boxHuella = document.getElementById("contenedor-huella");
                    const estadoLectura = document.getElementById("estado-lectura");
                    const inputHuella = document.getElementById("huella");

                    if (data.status === "success") {
                        // 1. Cambiar visualmente a estado de Éxito (Verde)
                        boxHuella.classList.add("capturada");
                        estadoLectura.style.color = "#27AE60";
                        estadoLectura.innerHTML = `✓ MARCADO PROCESADO CON ÉXITO`;
                        mostrarMensaje(data.message, "alert-success");

                        // 2. Limpieza automática tras 3 segundos para el siguiente personal
                        setTimeout(() => {
                            boxHuella.classList.remove("capturada");
                            estadoLectura.style.color = "#333333";
                            estadoLectura.innerHTML = "ESPERANDO ACCIÓN DEL PERSONAL...";
                            inputHuella.value = ""; // Limpia los puntos ••••••••
                            inputHuella.focus();    // Reenfoca el cursor automáticamente
                        }, 3000);

                    } else {
                        // 3. Manejo de Incidencias o Errores (Rojo / Naranja)
                        estadoLectura.style.color = "#E74C3C";
                        estadoLectura.innerHTML = `❌ VERIFICACIÓN RECHAZADA`;

                        if (data.status === "invalid" || data.status === "warning") {
                            mostrarMensaje(data.message, "alert-warning");
                        } else {
                            mostrarMensaje(data.message, "alert-danger");
                        }

                        // Limpiar el estado de error tras 4 segundos para permitir reintentar
                        setTimeout(() => {
                            estadoLectura.style.color = "#333333";
                            estadoLectura.innerHTML = "ESPERANDO ACCIÓN DEL PERSONAL...";
                            inputHuella.value = "";
                            inputHuella.focus();
                        }, 4000);
                    }
                })
        }, "image/jpeg");
    });

    // Función auxiliar para renderizar alertas dinámicas en pantalla
    function mostrarMensaje(texto, claseAlerta) {
        mensajeSistema.className = `alert mt-3 ${claseAlerta}`;
        mensajeSistema.innerText = texto;
        mensajeSistema.classList.remove("d-none");
    }
});
