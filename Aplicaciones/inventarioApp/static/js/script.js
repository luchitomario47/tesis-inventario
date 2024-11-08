// Función para obtener datos del localStorage
function obtenerInventario() {
    return JSON.parse(localStorage.getItem('inventario')) || [];
}

// Función para guardar inventario en el localStorage
function guardarInventario(inventario) {
    localStorage.setItem('inventario', JSON.stringify(inventario));
}

// Función para renderizar la tabla de inventario
function renderizarInventario() {
    const inventarioBody = document.getElementById('inventarioBody');
    inventarioBody.innerHTML = ''; // Limpiar la tabla
    const inventario = obtenerInventario();

    // Ordenar el inventario por fecha (más reciente primero)
    inventario.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));

    inventario.forEach((item) => {
        const row = `
            <tr>
                <td>${item.sku}</td>
                <td>${item.Modelo}</td>
                <td>${item.zona}</td>
                <td>${item.cantidad}</td>
                <td>${item.fecha}</td>
            </tr>
        `;
        inventarioBody.insertAdjacentHTML('beforeend', row);
    });
}

// Función para agregar un nuevo item al inventario
function agregarItem() {
    const tienda = document.getElementById('tiendaSelect');
    const zona = document.getElementById('zonaInput');
    const cantidad = document.getElementById('cantidadInput');
    const sku = document.getElementById('skuInput');

    if (tienda.value && zona.value && cantidad.value && sku.value) {
        const nuevoItem = {
            sku: sku.value,
            Modelo: "modelo",
            zona: zona.value,
            cantidad: cantidad.value,
            fecha: new Date().toLocaleString() // Fecha y hora actual
        };

        const inventario = obtenerInventario();
        inventario.unshift(nuevoItem); // Agregar al inicio de la lista
        guardarInventario(inventario);
        renderizarInventario();

        // Limpiar campo SKU y bloquear Tienda y Zona
        sku.value = '';
        tienda.disabled = true;
        zona.disabled = true;
    } else {
        alert('Por favor, completa todos los campos');
    }
}

// Función para enviar el inventario
document.getElementById('enviarBtn').addEventListener('click', function () {
    const inventario = obtenerInventario();
    console.log('Enviar inventario:', inventario);
    
    // Aquí puedes enviar el inventario al servidor con AJAX o fetch()
    // Luego de enviar, limpiar localStorage, tabla e inputs
    localStorage.removeItem('inventario');
    renderizarInventario();

    // Limpiar los campos y desbloquear Tienda y Zona
    document.getElementById('tiendaSelect').disabled = false;
    document.getElementById('zonaInput').disabled = false;
    document.getElementById('skuInput').value = '';
    document.getElementById('cantidadInput').value = '';
});

// Inicializar la tabla de inventario y la fecha cuando se cargue la página
document.addEventListener('DOMContentLoaded', function () {
    establecerFechaActual();
    renderizarInventario();
});

// Escuchar la tecla Enter en el campo SKU para agregar el elemento
document.getElementById('skuInput').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Evitar el comportamiento por defecto
        agregarItem(); // Llamar a la función para agregar el item
    }
});

// Función para establecer la fecha actual en el campo de entrada
function establecerFechaActual() {
    const fechaInput = document.getElementById('fechaInput');
    const fechaActual = new Date();
    
    // Formato de la fecha (YYYY-MM-DD) para el input tipo date
    const anio = fechaActual.getFullYear();
    const mes = String(fechaActual.getMonth() + 1).padStart(2, '0'); // Mes entre 1 y 12
    const dia = String(fechaActual.getDate()).padStart(2, '0'); // Día entre 1 y 31

    // Establecer el valor del campo de fecha
    fechaInput.value = `${anio}-${mes}-${dia}`;
}
