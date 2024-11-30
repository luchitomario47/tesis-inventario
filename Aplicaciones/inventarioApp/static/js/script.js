// Función para obtener datos del localStorage
function obtenerInventario() {
    return JSON.parse(localStorage.getItem('inventario')) || [];
}

// Función para obtener la cabecera
function obtenerCabecera(){
    return JSON.parse(localStorage.getItem('invCab')) || [];
}

// Función para guardar inventario en el localStorage
function guardarInventario(inventario) {
    localStorage.setItem('inventario', JSON.stringify(inventario));
}

// Función para registrar o actualizar la cabecera en el localStorage
function crearCabecera() {
    const tienda = document.getElementById('tiendaSelect').value; // Obtener el valor seleccionado
    const zona = document.getElementById('zonaInput').value; // Obtener el valor de la zona

    // Generar la fecha en formato YYYYMMDD
    const fechaActual = new Date();
    const anio = fechaActual.getFullYear();
    const mes = String(fechaActual.getMonth() + 1).padStart(2, '0'); // Mes con dos dígitos
    const dia = String(fechaActual.getDate()).padStart(2, '0'); // Día con dos dígitos
    const fechaFormato = `${anio}${mes}${dia}`; // Concatenar la fecha en formato YYYYMMDD

    // Crear el idInv concatenando la fecha con el número de la tienda
    const idInv = `${fechaFormato}${tienda}`;

    // Crear el objeto para guardar en el localStorage
    const cabecera = {
        tienda: tienda,
        zona: zona,
        idInv: idInv
    };

    // Guardar el objeto en el localStorage bajo la clave "invCab"
    localStorage.setItem('invCab', JSON.stringify(cabecera));
}

// Función para asegurarse de que `invCab` tenga la zona correcta
function actualizarZonaCabecera() {
    const zona = document.getElementById('zonaInput').value;

    // Obtener la cabecera existente
    const cabecera = JSON.parse(localStorage.getItem('invCab')) || {};

    // Actualizar la zona en la cabecera si existe
    if (zona) {
        cabecera.zona = zona;
        localStorage.setItem('invCab', JSON.stringify(cabecera));
    }
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

// Función para renderizar cabecera
function renderizarCabecera() {
    const cabecera = obtenerCabecera(); // Obtener la cabecera del localStorage

    if (!cabecera || Object.keys(cabecera).length === 0) {
        console.log("Cabecera no encontrada en localStorage.");
        return;
    }

    // Verificar si la cabecera tiene los campos necesarios
    const { tienda, zona } = cabecera;

    // Asignar valores a los campos HTML
    const tiendaSelect = document.getElementById('tiendaSelect');
    const zonaInput = document.getElementById('zonaInput');

    if (tienda) {
        tiendaSelect.value = tienda; // Seleccionar la tienda en el select
        tiendaSelect.disabled = true;
    }

    if (zona) {
        zonaInput.value = zona; // Rellenar el campo de zona
        zonaInput.disabled = true;
    }
}


renderizarCabecera();

// Función para agregar un nuevo item al inventario
function agregarItem() {
    const tienda = document.getElementById('tiendaSelect');
    const zona = document.getElementById('zonaInput');
    const cantidad = document.getElementById('cantidadInput');
    const sku = document.getElementById('skuInput');

    // Crear la cabecera solo si no existe en localStorage
    if (!localStorage.getItem('invCab')) {
        crearCabecera(); // Llamar a la función para crear la cabecera
    } else {
        actualizarZonaCabecera(); // Asegurar que la zona esté actualizada
    }

    // Obtener el idInv de la cabecera
    const cabecera = JSON.parse(localStorage.getItem('invCab')) || {};
    const idInventario = cabecera.idInv || 'Sin ID';

    // Verificar que todos los campos estén completos
    if (tienda.value && zona.value && cantidad.value && sku.value) {
        const nuevoItem = {
            idInventario: idInventario,
            sku: sku.value,
            Modelo: sku.value.slice(0, 9), // Extraer los primeros 9 caracteres del SKU
            zona: zona.value,
            cantidad: cantidad.value,
            fecha: new Date().toLocaleString() // Fecha y hora actual
        };

        // Guardar en el inventario
        const inventario = obtenerInventario();
        inventario.unshift(nuevoItem); // Agregar al inicio de la lista
        guardarInventario(inventario);
        renderizarInventario();

        // Limpiar campo SKU y bloquear Tienda y Zona
        sku.value = '';
        tienda.disabled = true;
        zona.disabled = true;
    } else {
        // Usar SweetAlert en lugar de alert
        Swal.fire({
            icon: 'warning',
            title: 'Campos incompletos',
            text: 'Por favor, completa todos los campos.',
            confirmButtonText: 'Aceptar'
        });
    }
}


// Función para enviar el inventario
document.getElementById('enviarBtn').addEventListener('click', function () {
    actualizarZonaCabecera(); // Actualizar zona antes de enviar

    const invCab = JSON.parse(localStorage.getItem('invCab'));
    const inventario = obtenerInventario();

    if (!invCab || !invCab.zona) {
        Swal.fire({
            icon: 'error',
            title: 'Datos incompletos',
            text: 'Por favor, asegúrate de completar la zona antes de enviar.',
            confirmButtonText: 'Aceptar'
        });
        return;
    }

    Swal.fire({
        title: '¿Estás seguro?',
        text: 'Esta acción enviará la información a la base de datos. Este proceso es irreversible. ¿Quieres continuar?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, enviar',
        cancelButtonText: 'Cancelar',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            console.log('Enviar cabecera:', invCab);
            console.log('Enviar inventario:', inventario);

            // Después de enviar, limpiar localStorage, tabla e inputs
            localStorage.removeItem('inventario');
            localStorage.removeItem('invCab');
            renderizarInventario();

            // Limpiar los campos y desbloquear Tienda y Zona
            document.getElementById('tiendaSelect').disabled = false;
            document.getElementById('tiendaSelect').value = '';
            document.getElementById('zonaInput').disabled = false;
            document.getElementById('zonaInput').value = '';
            document.getElementById('skuInput').value = '';
            document.getElementById('cantidadInput').disabled = true;

            Swal.fire('Enviado', 'El inventario ha sido enviado correctamente.', 'success');
        }
    });
});

// Función para establecer la fecha actual en el campo de entrada
function establecerFechaActual() {
    const fechaInput = document.getElementById('fechaInput');
    const fechaActual = new Date();

    // Formato de la fecha (YYYY-MM-DD) para el input tipo date
    const anio = fechaActual.getFullYear();
    const mes = String(fechaActual.getMonth() + 1).padStart(2, '0');
    const dia = String(fechaActual.getDate()).padStart(2, '0');

    // Establecer el valor del campo de fecha
    fechaInput.value = `${anio}-${mes}-${dia}`;
}

// Función para limpiar todo
document.getElementById('limpiarBtn').addEventListener('click', function () {
    Swal.fire({
        title: '¿Está seguro que quiere limpiar todo?',
        text: "¡Esta acción no se puede deshacer!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, limpiar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            localStorage.removeItem('inventario');
            localStorage.removeItem('invCab'); // Limpiar también la cabecera
            renderizarInventario();

            document.getElementById('tiendaSelect').disabled = false;
            document.getElementById('tiendaSelect').value = '';
            document.getElementById('zonaInput').disabled = false;
            document.getElementById('zonaInput').value = '';
            document.getElementById('skuInput').value = '';
            document.getElementById('cantidadInput').disabled = true;

            Swal.fire(
                'Limpio',
                'El inventario ha sido limpiado.',
                'success'
            );
        }
    });
});

// Escuchar el evento de clic en el botón Agregar
document.getElementById('agregarBtn').addEventListener('click', function () {
    agregarItem(); // Llamar a la función para agregar el item
});

// Escuchar la tecla Enter en el campo SKU para agregar el elemento
document.getElementById('skuInput').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        agregarItem(); // Llamar a la función para agregar el item
    }
});

// Inicializar la tabla de inventario y la fecha cuando se cargue la página
document.addEventListener('DOMContentLoaded', function () {
    establecerFechaActual();
    renderizarInventario();
});
// Función para actualizar el contador

function actualizarContador() {
    const inventario = obtenerInventario(); // Obtener el inventario desde localStorage
    const contadorElementos = document.getElementById('contadorElementos'); // Elemento donde se muestra el contador
    contadorElementos.value = inventario.length; // Actualizar el contador con la cantidad de elementos
}
const inventario = obtenerInventario();
console.log(inventario.length);
