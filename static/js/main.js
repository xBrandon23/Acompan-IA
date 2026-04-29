// ========================================
// JavaScript - Acompan-IA
// ========================================

// ========== UTILIDADES ==========

/**
 * Mostrar una notificación toast
 */
function mostrarToast(mensaje, tipo = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${tipo} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(toast);

    // Auto-remove después de 5 segundos
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

/**
 * Formatear fecha
 */
function formatearFecha(fecha) {
    if (typeof fecha === 'string') {
        fecha = new Date(fecha);
    }
    return fecha.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Obtener color basado en el nivel de riesgo
 */
function getColorRiesgo(nivel) {
    const colores = {
        'bajo': '#27ae60',
        'medio': '#f39c12',
        'alto': '#e74c3c',
        'critico': '#8b0000'
    };
    return colores[nivel] || '#666';
}

/**
 * Obtener badge HTML basado en el nivel de riesgo
 */
function getBadgeRiesgo(nivel) {
    const estilos = {
        'bajo': 'success',
        'medio': 'warning',
        'alto': 'danger',
        'critico': 'dark'
    };
    return `<span class="badge bg-${estilos[nivel]}">${nivel.toUpperCase()}</span>`;
}

// ========== VALIDACIONES ==========

/**
 * Validar email
 */
function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Validar contraseña (mínimo 6 caracteres)
 */
function validarPassword(password) {
    return password.length >= 6;
}

/**
 * Validar formulario antes de enviar
 */
function validarFormulario(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let valido = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            valido = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });

    return valido;
}

// ========== FUNCIONES DE GRÁFICOS ==========

/**
 * Crear gráfico de distribución
 */
function crearGraficoDistribucion(elementId, datos, etiquetas) {
    const ctx = document.getElementById(elementId);
    if (!ctx) return;

    const colores = ['#27ae60', '#f39c12', '#e74c3c', '#8b0000'];

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: etiquetas,
            datasets: [{
                data: datos,
                backgroundColor: colores
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

/**
 * Crear gráfico de línea
 */
function crearGraficoLinea(elementId, labels, datos, label) {
    const ctx = document.getElementById(elementId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: datos,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                }
            }
        }
    });
}

// ========== FUNCIONES DE TABLA ==========

/**
 * Filtrar tabla por texto
 */
function filtrarTabla(inputId, tableId) {
    const input = document.getElementById(inputId);
    const tabla = document.getElementById(tableId);
    const filas = tabla.querySelectorAll('tbody tr');

    input.addEventListener('keyup', function() {
        const filtro = this.value.toLowerCase();

        filas.forEach(fila => {
            const texto = fila.textContent.toLowerCase();
            fila.style.display = texto.includes(filtro) ? '' : 'none';
        });
    });
}

/**
 * Ordenar tabla por columna
 */
function ordenarTabla(tableId, columnIndex) {
    const tabla = document.getElementById(tableId);
    const tbody = tabla.querySelector('tbody');
    const filas = Array.from(tbody.querySelectorAll('tr'));

    const ordenAscendente = tabla.dataset.orden !== 'asc';
    tabla.dataset.orden = ordenAscendente ? 'asc' : 'desc';

    filas.sort((a, b) => {
        const celdaA = a.querySelectorAll('td')[columnIndex];
        const celdaB = b.querySelectorAll('td')[columnIndex];

        const valorA = celdaA.textContent.trim();
        const valorB = celdaB.textContent.trim();

        // Intentar convertir a números si es posible
        const numA = parseFloat(valorA);
        const numB = parseFloat(valorB);

        if (!isNaN(numA) && !isNaN(numB)) {
            return ordenAscendente ? numA - numB : numB - numA;
        }

        // Comparación de strings
        return ordenAscendente
            ? valorA.localeCompare(valorB)
            : valorB.localeCompare(valorA);
    });

    // Re-agregar las filas ordenadas
    filas.forEach(fila => tbody.appendChild(fila));
}

// ========== FUNCIONES DEL CHAT ==========

/**
 * Auto-scroll al final del chat
 */
function autoScrollChat(elementId) {
    const elemento = document.getElementById(elementId);
    if (elemento) {
        setTimeout(() => {
            elemento.scrollTop = elemento.scrollHeight;
        }, 100);
    }
}

/**
 * Formatear mensaje para mostrar
 */
function formatearMensaje(mensaje, esEstudiante = true) {
    const claseDiv = `chat-message ${esEstudiante ? 'estudiante' : 'ia'}`;
    const ahora = new Date();
    const hora = ahora.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });

    return `
        <div class="${claseDiv}">
            <div>
                <div class="message-content">${mensaje}</div>
                <div class="message-time">${hora}</div>
            </div>
        </div>
    `;
}

// ========== FUNCIONES DE API ==========

/**
 * Hacer petición GET
 */
async function hacerPeticionGET(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        mostrarToast('Error al realizar la solicitud', 'danger');
        return null;
    }
}

/**
 * Hacer petición POST
 */
async function hacerPeticionPOST(url, datos) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        mostrarToast('Error al realizar la solicitud', 'danger');
        return null;
    }
}

// ========== FUNCIONES DE INICIALIZACIÓN ==========

/**
 * Inicializar tooltips de Bootstrap
 */
function inicializarTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

/**
 * Inicializar popovers de Bootstrap
 */
function inicializarPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
}

// ========== EVENT LISTENERS ==========

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips
    inicializarTooltips();

    // Inicializar popovers
    inicializarPopovers();

    // Agregar estilos de validación a los formularios
    const formularios = document.querySelectorAll('form');
    formularios.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity() === false) {
                e.preventDefault();
                e.stopPropagation();
            }
            this.classList.add('was-validated');
        });
    });
});

// ========== FUNCIONES DE UTILIDAD ==========

/**
 * Copiar texto al portapapeles
 */
function copiarAlPortapapeles(texto) {
    navigator.clipboard.writeText(texto).then(() => {
        mostrarToast('Copiado al portapapeles', 'success');
    }).catch(() => {
        mostrarToast('Error al copiar', 'danger');
    });
}

/**
 * Descargar archivo
 */
function descargarArchivo(url, nombre) {
    const enlace = document.createElement('a');
    enlace.href = url;
    enlace.download = nombre;
    document.body.appendChild(enlace);
    enlace.click();
    document.body.removeChild(enlace);
}

/**
 * Confirmar acción
 */
function confirmarAccion(mensaje = '¿Estás seguro?') {
    return confirm(mensaje);
}

// ========== FUNCIONES DE TEMAS ==========

/**
 * Cambiar tema (claro/oscuro)
 */
function cambiarTema() {
    const htmlElement = document.documentElement;
    const temaActual = htmlElement.getAttribute('data-bs-theme');
    const nuevoTema = temaActual === 'dark' ? 'light' : 'dark';

    htmlElement.setAttribute('data-bs-theme', nuevoTema);
    localStorage.setItem('tema', nuevoTema);
}

/**
 * Cargar tema guardado
 */
function cargarTemaSaved() {
    const temaGuardado = localStorage.getItem('tema') || 'light';
    document.documentElement.setAttribute('data-bs-theme', temaGuardado);
}

// Cargar tema al cargar la página
window.addEventListener('load', cargarTemaSaved);

// ========== DEPURACIÓN ==========

/**
 * Log condicional (solo en desarrollo)
 */
function log(mensaje, datos = null) {
    if (window.DEBUG) {
        console.log(`[LOG] ${mensaje}`, datos || '');
    }
}
