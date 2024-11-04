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

    inventario.forEach((item) => {
        const row = `
            <tr>
                <td>${item.sku}</td>
                <td>${item.sku}</td>
                <td>${item.zona}</td>
                <td>${item.cantidad}</td>
                <td>${item.fecha}</td>
            </tr>
        `;
        inventarioBody.insertAdjacentHTML('beforeend', row);
    });
}

// Función para agregar un nuevo item al inventario
document.getElementById('agregarBtn').addEventListener('click', function () {
    const tienda = document.getElementById('tiendaSelect').value;
    const zona = document.getElementById('zonaInput').value;
    const cantidad = document.getElementById('cantidadInput').value;
    const sku = document.getElementById('skuInput').value;

    if (tienda && zona && cantidad && sku) {
        const nuevoItem = {
            sku: sku,
            Modelo: "modelo",
            Zona: zona,
            Cantidad: cantidad,
            fecha: new Date().toLocaleString() // Fecha y hora actual
        };

        const inventario = obtenerInventario();
        inventario.push(nuevoItem);
        guardarInventario(inventario);
        renderizarInventario();
    } else {
        alert('Por favor, completa todos los campos');
    }
});

// Función para enviar el inventario (aquí puedes agregar tu lógica de envío)
document.getElementById('enviarBtn').addEventListener('click', function () {
    const inventario = obtenerInventario();
    console.log('Enviar inventario:', inventario);
    // Aquí puedes enviar el inventario al servidor con AJAX o fetch()
});

// Inicializar la tabla de inventario cuando se cargue la página
document.addEventListener('DOMContentLoaded', function () {
    renderizarInventario();
});

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
                <td>${item.sku}</td>
                <td>${item.zona}</td>
                <td>${item.cantidad}</td>
                <td>${item.fecha}</td>
            </tr>
        `;
        inventarioBody.insertAdjacentHTML('beforeend', row);
    });
}


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

// Inicializar la fecha al cargar la página
document.addEventListener('DOMContentLoaded', function () {
    establecerFechaActual();
    renderizarInventario();
});
