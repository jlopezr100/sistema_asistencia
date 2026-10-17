document.addEventListener("DOMContentLoaded", function () {
    const inputHuella = document.getElementById("huella");
    const formAsistencia = document.getElementById("form-asistencia");
    const mensajeSistema = document.getElementById("mensaje-sistema");
    const boxHuella = document.getElementById("contenedor-huella");
    const estadoLectura = document.getElementById("estado-lectura");

    // Mantener el foco automático en el campo del lector de fondo
    if (inputHuella) {
        inputHuella.focus();
        document.addEventListener("click", () => {
            setTimeout(() => { inputHuella.focus(); }, 500);
        });
    }

    // Interceptar el envío automático del sensor biométrico
    if (inputHuella) {
        inputHuella.addEventListener("keydown", function (event) {
            if (event.key === "Enter" || event.keyCode === 13) {
                event.preventDefault(); // Evita recargar la página

                const huellaValor = inputHuella.value.trim();
                const lat = document.getElementById("latitud").value || "0";
                const lon = document.getElementById("longitud").value || "0";

                if (!huellaValor) return;

                // Cambiar estado a búsqueda activa
                if (estadoLectura) estadoLectura.innerHTML = "BUSCANDO PERSONAL...";
                if (mensajeSistema) mensajeSistema.classList.add("d-none");

                // Capturar el fotograma de fondo (Canvas oculto)
                const video = document.getElementById("video");
                const canvas = document.getElementById("canvas");
                const context = canvas.getContext("2d");
                
                if (video && canvas) {
                    canvas.width = video.videoWidth || 640;
                    canvas.height = video.videoHeight || 480;
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                }

                // Función interna para procesar el envío del formulario con o sin blob
                const enviarData = (blob) => {
                    const formData = new FormData();
                    formData.append("huella", huellaValor);
                    formData.append("latitud", lat);
                    formData.append("longitud", lon);
                    formData.append("serie_dispositivo", "PC-LOCAL-NAVEGADOR");
                    if (blob) {
                        formData.append("ubicacion_imagen", blob, `marcado_${Date.now()}.jpg`);
                    }

                    fetch("/asistencia/api/registrar/", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (mensajeSistema) mensajeSistema.classList.remove("d-none");

                        if (data.status === "success") {
                            if (boxHuella) boxHuella.classList.add("capturada");
                            if (estadoLectura) estadoLectura.innerHTML = "✓ IDENTIDAD VERIFICADA";
                            
                            if (mensajeSistema) {
                                mensajeSistema.className = "alert alert-success text-center font-weight-bold shadow-sm";
                                mensajeSistema.innerHTML = data.message;
                            }
                            
                            setTimeout(() => {
                                if (boxHuella) boxHuella.classList.remove("capturada");
                                if (estadoLectura) estadoLectura.innerHTML = "Coloque el dedo en el lector";
                                if (mensajeSistema) mensajeSistema.classList.add("d-none");
                                inputHuella.value = "";
                                inputHuella.focus();
                            }, 3000);

                        } else {
                            if (boxHuella) boxHuella.classList.remove("capturada");
                            if (estadoLectura) estadoLectura.innerHTML = "❌ ACCESO DENEGADO";
                            
                            if (mensajeSistema) {
                                mensajeSistema.className = "alert alert-danger text-center font-weight-bold shadow-sm";
                                mensajeSistema.innerHTML = data.message;
                            }

                            setTimeout(() => {
                                if (estadoLectura) estadoLectura.innerHTML = "Coloque el dedo en el lector";
                                if (mensajeSistema) mensajeSistema.classList.add("d-none");
                                inputHuella.value = "";
                                inputHuella.focus();
                            }, 4000);
                        }
                    })
                    .catch(error => {
                        if (estadoLectura) estadoLectura.innerHTML = "Coloque el dedo en el lector";
                        if (mensajeSistema) {
                            mensajeSistema.classList.remove("d-none");
                            mensajeSistema.className = "alert alert-danger text-center font-weight-bold";
                            mensajeSistema.innerHTML = "⚠️ Error de comunicación con el servidor.";
                        }
                        inputHuella.value = "";
                    });
                };

                // Si hay canvas válido genera el blob, si no, envía directo para no trabar el flujo
                if (canvas && video && video.srcObject) {
                    canvas.toBlob(enviarData, "image/jpeg");
                } else {
                    enviarData(null);
                }
            }
        });
    }

    // Capturar coordenadas GPS automáticamente de fondo
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(function (position) {
            const latInput = document.getElementById("latitud");
            const lonInput = document.getElementById("longitud");
            if (latInput) latInput.value = position.coords.latitude;
            if (lonInput) lonInput.value = position.coords.longitude;
        }, null, { enableHighAccuracy: true });
    }
});
