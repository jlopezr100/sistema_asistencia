/**
 * Lógica JavaScript para el Módulo de Máquinas
 */

function abrirModalAnularConData(btn) {
    const url = btn.getAttribute('data-url');
    const nombre = btn.getAttribute('data-nombre');
    
    const formEliminar = document.getElementById('form-eliminar');
    if (formEliminar) {
        formEliminar.action = url;
    }
    
    const tituloRegistro = document.getElementById('modal-registro-titulo');
    if (tituloRegistro) {
        tituloRegistro.textContent = nombre;
    }
    
    const modal = document.getElementById('modal-confirmacion');
    if (modal) {
        if (typeof modal.showModal === "function") {
            modal.showModal();
        } else {
            modal.style.display = 'block';
        }
    }
}

function cerrarModalGlobal() {
    const modal = document.getElementById('modal-confirmacion');
    if (modal) {
        if (typeof modal.close === "function") {
            modal.close();
        } else {
            modal.style.display = 'none';
        }
    }
}
