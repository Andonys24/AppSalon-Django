let paso = 1;
const pasoInicial = 1;
const pasoFinal = 3;

const cita = {
	id: "",
	nombre: "",
	fecha: "",
	hora: "",
	servicios: [],
};

document.addEventListener("DOMContentLoaded", function () {
	iniciarApp();
});

function iniciarApp() {
	mostrarSeccion(); // Muestra y oculta las secciones
	tabs(); //Cambiar la seccion cuando se presionen los tabs
	botonesPaginador(); // Agrega o quita los botones paginadores
	paginaAnterior();
	paginaSiguiente();

	consultarAPI(); // Consulta la api en el backend de PHP

	idCliente(); //
	nombreCliente(); // Añade el nombre del cliente al objeto de cita
	seleccionarFecha(); // Añade la fecha de la cita en el objeto
	seleccionarHora(); // Añade la hora de la cita en el objeto

	mostrarResumen(); // Muestra el resumen de la cita
}

function mostrarSeccion() {
	// Ocultar la seccion que tenga la clase mostrar
	const seccionAnterior = document.querySelector(".mostrar");
	if (seccionAnterior) {
		seccionAnterior.classList.remove("mostrar");
	}

	// Seleccionar la seccion con el paso...
	const seccion = document.querySelector(`#paso-${paso}`);
	seccion.classList.add("mostrar");

	// Quita la clase de actual al tab anterior
	const tabAnterior = document.querySelector(".actual");
	if (tabAnterior) {
		tabAnterior.classList.remove("actual");
	}

	// Resalta el tab actual
	const tab = document.querySelector(`[data-paso="${paso}"]`);
	tab.classList.add("actual");
}

function tabs() {
	const botones = document.querySelectorAll(".tabs button");

	botones.forEach((boton) => {
		boton.addEventListener("click", function (e) {
			paso = parseInt(e.target.dataset.paso);

			mostrarSeccion();
			botonesPaginador();
		});
	});
}

function botonesPaginador() {
	const paginaAnterior = document.querySelector("#anterior");
	const paginaSiguiente = document.querySelector("#siguiente");

	if (paso === pasoInicial) {
		paginaAnterior.classList.add("ocultar");
		paginaSiguiente.classList.remove("ocultar");
	} else if (paso === pasoFinal) {
		paginaAnterior.classList.remove("ocultar");
		paginaSiguiente.classList.add("ocultar");

		mostrarResumen();
	} else {
		paginaAnterior.classList.remove("ocultar");
		paginaSiguiente.classList.remove("ocultar");
	}
	mostrarSeccion();
}
function paginaAnterior() {
	const paginaAnterior = document.querySelector("#anterior");
	paginaAnterior.addEventListener("click", function () {
		if (paso <= pasoInicial) return;
		paso--;
		botonesPaginador();
	});
}
function paginaSiguiente() {
	const paginaSiguiente = document.querySelector("#siguiente");
	paginaSiguiente.addEventListener("click", function () {
		if (paso >= pasoFinal) return;
		paso++;
		botonesPaginador();
	});
}

async function consultarAPI() {
	try {
		const url = "/api/servicios";
		const resultado = await fetch(url);
		const servicios = await resultado.json();
		mostrarServicios(servicios);
	} catch (error) {
		console.log(error);
	}
}

function mostrarServicios(servicios) {
	servicios.forEach((servicio) => {
		const { id, nombre, precio } = servicio;

		// Mostrando los nombres dentro de la etiqueta p
		const nombreServicio = document.createElement("P");
		nombreServicio.classList.add("nombre-servicio");
		nombreServicio.textContent = nombre;

		// Mostrando los precios en una etiqueta p
		const precioServicio = document.createElement("P");
		precioServicio.classList.add("precio-servicio");
		precioServicio.textContent = `L.${precio}`;

		// Creacion del div serivicio
		const servicioDiv = document.createElement("div");
		servicioDiv.classList.add("servicio");
		servicioDiv.dataset.idServicio = id;
		servicioDiv.onclick = function () {
			seleccionarServicio(servicio);
		};

		// Agregar los nombres y precios dentro del div de servicios
		servicioDiv.appendChild(nombreServicio);
		servicioDiv.appendChild(precioServicio);

		// Seleccionamos el div con la clase servicio y inyectamos los datos del div dentro
		document.querySelector("#servicios").appendChild(servicioDiv);
	});
}

function seleccionarServicio(servicio) {
	const { id } = servicio;
	const { servicios } = cita;

	// Identificar el elemento que se le da el click
	const divServicio = document.querySelector(`[data-id-servicio="${id}"]`);
	// Comprobar si un servicio ya fue agregado
	if (servicios.some((agregado) => agregado.id === servicio.id)) {
		// Eliminarlo
		cita.servicios = servicios.filter((agregado) => agregado.id != id);
		divServicio.classList.remove("seleccionado");
	} else {
		// Agregarlo
		cita.servicios = [...servicios, servicio];
		divServicio.classList.add("seleccionado");
	}
}

function idCliente() {
	cita.id = document.querySelector("#id").value;
}

function nombreCliente() {
	cita.nombre = document.querySelector("#nombre").value;
}

function seleccionarFecha() {
	const inputFecha = document.querySelector("#fecha");
	inputFecha.addEventListener("input", function (e) {
		const dia = new Date(e.target.value).getUTCDay();

		if ([6, 0].includes(dia)) {
			// Si es Sabado y domingo no permitimos los valores
			e.target.value = "";
			mostrarAlerta("Fines de semana no permitidos.", "error", ".formulario");
		} else {
			// Si es correcto agregamos al arreglo
			cita.fecha = e.target.value;
		}
	});
}

function seleccionarHora() {
	const inputHora = document.querySelector("#hora");
	inputHora.addEventListener("input", function (e) {
		const horaCita = e.target.value;
		const hora = horaCita.split(":")[0];
		if (hora < 10 || hora > 19) {
			e.target.value = "";
			mostrarAlerta("Hora No Valida.", "error", ".formulario");
		} else {
			cita.hora = e.target.value;
		}
	});
}

function mostrarAlerta(mensaje, tipo, elemento, desaparece = true) {
	// Prevenir que se genere mas de una alerta
	const alertaPrevia = document.querySelector(".alerta");
	if (alertaPrevia) {
		alertaPrevia.remove();
	}

	// Script para crear la alerta
	const alerta = document.createElement("DIV");
	alerta.textContent = mensaje;
	alerta.classList.add("alerta");
	alerta.classList.add(tipo);

	const referencia = document.querySelector(elemento);
	referencia.appendChild(alerta);

	if (desaparece) {
		// Eliminar la alerta
		setTimeout(() => {
			alerta.remove();
		}, 3000);
	}
}

function mostrarResumen() {
	const resumen = document.querySelector(".contenido-resumen");

	// Limpiar el contenido del resumen
	while (resumen.firstChild) {
		resumen.removeChild(resumen.firstChild);
	}

	// Con Object.value podemos validar los objetos si estan vacios o no
	if (Object.values(cita).includes("") || cita.servicios.length === 0) {
		mostrarAlerta("Faltan datos de Servicios, fecha u Hora", "error", ".contenido-resumen", false);
		return;
	}
	// Formatear el div de resumen
	const { nombre, fecha, hora, servicios } = cita;

	// Heading para servicios Resumen
	const headingServicios = document.createElement("h3");
	headingServicios.textContent = "Resumen de Servicios";
	resumen.appendChild(headingServicios);

	// Iteramos y mostramos los servicios
	servicios.forEach((servicio) => {
		const { id, precio, nombre } = servicio;
		const contenedorServicio = document.createElement("div");
		contenedorServicio.classList.add("contenedor-servicio");

		const textoServicio = document.createElement("p");
		textoServicio.textContent = nombre;

		const precioServicio = document.createElement("P");
		precioServicio.innerHTML = `<span>Precio:</span> L.${precio}`;

		contenedorServicio.appendChild(textoServicio);
		contenedorServicio.appendChild(precioServicio);

		resumen.appendChild(contenedorServicio);
	});

	// Heading para Cita Resumen
	const headingCita = document.createElement("h3");
	headingCita.textContent = "Resumen de Cita";
	resumen.appendChild(headingCita);

	const nombreCliente = document.createElement("P");
	nombreCliente.innerHTML = `<span>Nombre:</span> ${nombre}.`;

	// Formatear la fecha en español
	const fechaObj = new Date(fecha);
	const mes = fechaObj.getMonth();
	const dia = fechaObj.getDate() + 2;
	const year = fechaObj.getFullYear();

	const opciones = { weekday: "long", day: "numeric", month: "long", year: "numeric" };
	const fechaUTC = new Date(Date.UTC(year, mes, dia));
	const fechaFormateada = fechaUTC.toLocaleDateString("es-MX", opciones);

	const fechaCita = document.createElement("P");
	fechaCita.innerHTML = `<span>Fecha:</span> ${fechaFormateada}.`;

	const horaCita = document.createElement("P");
	horaCita.innerHTML = `<span>Hora:</span> ${hora} Horas.`;

	// Boton para Crear una Cita
	const botonReserva = document.createElement("button");
	botonReserva.classList.add("boton");
	botonReserva.textContent = "Reservar Cita";
	botonReserva.onclick = reservarCita;

	resumen.appendChild(nombreCliente);
	resumen.appendChild(fechaCita);
	resumen.appendChild(horaCita);
	resumen.appendChild(botonReserva);
}

async function reservarCita() {
	const { id, nombre, fecha, hora, servicios } = cita;

	const idServicios = servicios.map((servicio) => servicio.id);

	const datos = new FormData();
	datos.append("usuario_id", id);
	datos.append("fecha", fecha);
	datos.append("hora", hora);
	datos.append("servicios", idServicios);

	try {
		// Peticion hacia la api
		// const url = `${location.origin}/api/citas`;
		const url = "/api/citas";
		const respuesta = await fetch(url, {
			method: "POST",
			body: datos,
		});

		const resultado = await respuesta.json();

		if (resultado.resultado) {
			// Mostrando alerta de Cita creada con Sweetalert2
			Swal.fire({
				icon: "success",
				title: "Cita Creada",
				text: "Tu cita fue Creada Correctamente!",
				button: "OK",
			}).then(() => {
				setTimeout(() => {
					window.location.reload();
				}, 2000);
			});
		}
	} catch (error) {
		Swal.fire({
			icon: "error",
			title: "Error",
			text: "Hubo un error al guardar la cita!",
			button: "OK",
		});
	}

	// Ver datos de FormData()
	// console.log([...datos]);
}
