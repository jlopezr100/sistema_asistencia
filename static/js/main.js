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
    const inputHuella = document.getElementById("huella");
    const formAsistencia = document.getElementById("form-asistencia");

    // Mantener el cursor enfocado permanentemente en el input para lectura rápida
    if (inputHuella) {
        inputHuella.focus();
        document.addEventListener("click", () => {
            setTimeout(() => { inputHuella.focus(); }, 1500);
        });
    }

    // Detectar cuando el lector inyecta la huella y presiona "Enter" automáticamente
    if (inputHuella) {
        inputHuella.addEventListener("keydown", function (event) {
            // 13 es el código de la tecla Enter
            if (event.key === "Enter" || event.keyCode === 13) {
                event.preventDefault(); // Evita que la página se recargue de forma tradicional
                
                const huellaValor = inputHuella.value.trim();
                const lat = document.getElementById("latitud").value;
                const lon = document.getElementById("longitud").value;

                if (!huellaValor) return; // Si está vacío, no hace nada

                if (!lat || !lon) {
                    const mensajeSistema = document.getElementById("mensaje-sistema");
                    mensajeSistema.classList.remove("d-none");
                    mensajeSistema.className = "alert alert-warning text-center font-weight-bold";
                    mensajeSistema.innerHTML = "❌ Error: Esperando señal GPS válida... Intente en 2 segundos.";
                    return;
                }

                // Deshabilitar temporalmente el campo para evitar lecturas duplicadas seguidas
                inputHuella.disabled = true;

                // Capturar fotograma de fondo (Canvas oculto)
                const video = document.getElementById("video");
                const canvas = document.getElementById("canvas");
                const context = canvas.getContext("2d");
                canvas.width = video.videoWidth || 640;
                canvas.height = video.videoHeight || 480;
                context.drawImage(video, 0, 0, canvas.width, canvas.height);

                // Convertir la foto a binario y procesar el envío
                canvas.toBlob(function (blob) {
                    const formData = new FormData();
                    formData.append("huella", huellaValor);
                    formData.append("latitud", lat);
                    formData.append("longitud", lon);
                    formData.append("serie_dispositivo", "PC-LOCAL-NAVEGADOR");
                    formData.append("ubicacion_imagen", blob, `marcado_${Date.now()}.jpg`);

                    // Petición AJAX silenciosa a Django
                    fetch("/asistencia/api/registrar/", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        inputHuella.disabled = false; // Desbloquear campo para el siguiente usuario
                        const boxHuella = document.getElementById("contenedor-huella");
                        const mensajeSistema = document.getElementById("mensaje-sistema");

                        mensajeSistema.classList.remove("d-none");

                        if (data.status === "success") {
                            // --- REGISTRO CORRECTO ---
                            if (boxHuella) boxHuella.classList.add("capturada");
                            mensajeSistema.className = "alert alert-success text-center font-weight-bold shadow-sm";
                            mensajeSistema.innerHTML = `✓ ${data.message}`;
                            
                            setTimeout(() => {
                                if (boxHuella) boxHuella.classList.remove("capturada");
                                mensajeSistema.classList.add("d-none");
                                inputHuella.value = "";
                                inputHuella.focus();
                            }, 3000);

                        } else {
                            // --- USUARIO NO EXISTE O INCIDENCIAS ---
                            mensajeSistema.className = data.status === "invalid" 
                                ? "alert alert-warning text-center font-weight-bold shadow-sm"
                                : "alert alert-danger text-center font-weight-bold shadow-sm";
                            
                            mensajeSistema.innerHTML = `❌ ${data.message}`;

                            setTimeout(() => {
                                mensajeSistema.classList.add("d-none");
                                inputHuella.value = "";
                                inputHuella.focus();
                            }, 4000);
                        }
                    })
                    .catch(error => {
                        inputHuella.disabled = false;
                        const mensajeSistema = document.getElementById("mensaje-sistema");
                        mensajeSistema.classList.remove("d-none");
                        mensajeSistema.className = "alert alert-danger text-center font-weight-bold";
                        mensajeSistema.innerHTML = "⚠️ Error de red o comunicación fallida con el servidor.";
                    });
                }, "image/jpeg");
            }
        });
    }
});
