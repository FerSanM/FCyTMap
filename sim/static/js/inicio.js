const listarMaterias = async (idCarrera, Semestre) => {
    try {
        const response = await fetch(`materias/${idCarrera}/${Semestre}`, {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer my_secret_token'
            }
        });
        const data = await response.json();
        console.log(data);

        if (data.message === "Success") {

            let opciones = ``;
            data.materias.forEach((materia) => {
                opciones += `<input type="checkbox" name="materias" class="btn-check" id="${materia.id}" value="${materia.id}" autocomplete="off">
                                <label class="btn" id="btnmate" for="${materia.id}">${materia.descripcion}</label>`;
            })
            matecon.innerHTML = opciones


        } else {
            alert("datos no encontrados");
        }
    } catch (error) {
        console.log(error);
    }
}

const listarNotificaciones = async () => {
    try {
        const response = await fetch("notificaciones/", {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer my_secret_token'
            }
        });
        const data = await response.json();
        console.log(data);

        if (data.message === "Success") {
            let opciones = ``;
            let alerta = '';
            let tieneNotificacionesNoVistas = false;
            const maxNotificaciones = 6; // Máximo de notificaciones a mostrar
            const notificaciones = data.notificaciones.slice(0, maxNotificaciones);

            notificaciones.forEach((notificacion) => {
                const fechaFormateada = formatDate(notificacion.fecha_actividad);
                const diasFaltantes = calculateDaysDifference(notificacion.fecha_actividad);
                let actividadFin = new Date(notificacion.fecha_actividad);
                actividadFin.setHours(23, 59, 59, 999);
                let mensajeDias = '';
                if (notificacion.vistousuario === 0) {
                    tieneNotificacionesNoVistas = true;
                }

                if (new Date() >= new Date(notificacion.fecha_actividad)) {
                    if (new Date() >= new Date(notificacion.fecha_actividad) && new Date() <= actividadFin) {
                        mensajeDias = 'En Curso'
                    } else {
                        mensajeDias = 'Finalizado';
                    }
                } else {
                    if (diasFaltantes >= 1) {
                        mensajeDias = `Faltan ${diasFaltantes} días para el evento`;
                    } else {
                        const horasfaltantes = calculateHoursDifference(notificacion.fecha_actividad);
                        mensajeDias = `Faltan ${horasfaltantes}  para el evento`;
                    }
                }
                opciones += `
                    <li class="li-noti">
                        <a class="dropdown-item" href="#">
                            <div class="noti-container">
                                <div class="icon-noti">
                                    <i class="bi bi-journal-bookmark-fill"></i>
                                </div>
                                <div class="content-noti">
                                    <span style="font-size: 12px">Notificación de Evento</span><br>
                                    <span><b>${notificacion.descripcion}</b></span><br>
                                    <span style="font-size: 12px">${mensajeDias}</span>
                                     
                                </div>
                            </div>
                        </a>
                    </li>`;
            });
            if(tieneNotificacionesNoVistas){
                    alerta = "<span class=\"position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger\">\n" +
                        "                !\n" +
                        "                <span class=\"visually-hidden\">Notificaciones</span>"
                    iconnoti.innerHTML = alerta
            }else{
                iconnoti.innerHTML = alerta
            }
            // Verificar si hay más de 5 notificaciones para mostrar el "Ver Más"
            opciones += `
                    <li class="fixed-footer">
                        <footer class="footer-noti">
                            <a href="#">Ver Más</a>
                        </footer>
                    </li>`;

            document.getElementById('notif').innerHTML = opciones;

        } else {
            //alert("Sin Notificaciones Pendientes");
        }
    } catch (error) {
        console.log(error);
    }
};



const listarCarreras = async () => {
    try {
        const response = await fetch("carreras/", {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer my_secret_token'
            }
        });
        const data = await response.json();
        console.log(data);

        if (data.message === "Success") {

            let opciones = ``;
            data.carreras.forEach((carrera) => {
                opciones += `<option value="${carrera.id}">${carrera.descripcion}</option>`;
            })

            carrera.innerHTML = opciones

        } else {
            alert("datos no encontrados");
        }
    } catch (error) {
        console.log(error);
    }
};
const listarsalas = async () => {
    try {
        const response = await fetch("listarsalas/", {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer my_secret_token'
            }
        });
        const sala = await response.json();
        console.log(sala);

        if (sala.message === "Success") {

            let opciones = ``;
            opciones += `<option selected disabled value="">Elige una Ubicacion</option>`
            sala.salas.forEach((sala) => {
                opciones += `<option value="${sala.id}">${sala.descripcion}</option>`;
            })

            salas.innerHTML = opciones

        } else {
            alert("datos no encontrados");
        }
    } catch (error) {
        console.log(error);
    }
};
const listarsalasedit = async () => {
    try {
       const response = await fetch("listarsalas/", {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer my_secret_token'
            }
        });
        const sala = await response.json();
        console.log(sala);

        if (sala.message === "Success") {

            let opciones = ``;
            sala.salas.forEach((sala) => {
                opciones += `<option value="${sala.id}">${sala.descripcion}</option>`;
            })

            salasEditar.innerHTML = opciones

        } else {
            alert("datos no encontrados");
        }
    } catch (error) {
        console.log(error);
    }
};
const mostrarsemestre = () => {

    let opciones = ``;

    opciones = `<option value="1">Primero</option>
                <option value="2">Segundo</option>
                <option value="3">Tercero</option>
                <option value="4">Cuarto</option>
                <option value="5">Quinto</option>
                <option value="6">Sexto</option>
                <option value="7">Séptimo</option>
                <option value="8">Octavo</option>
                <option value="9">Noveno</option>
                <option value="10">Décimo</option>`;
    semestre.innerHTML = opciones

}

mostrarTabla = async () => {
    try {
        const response = await fetch("tabla/",{
            method: 'GET',
            headers: {
                'Authorization': 'Bearer my_secret_token'
            }
        });
        const data = await response.json();
        console.log(data);

        if (data.message === "Success") {

            let opciones = ``;
            data.datos.forEach((dato) => {
                opciones += `<tr>
                             <td>${dato.Materia}</td>
                             <td class="text-center">${dato.Semestre}</td>
                             <td class="text-center"><button type="button" class="btn btn-danger btn-eliminar" data-materia-id="${dato.id}" data-bs-toggle="modal" data-bs-target="#eliminarmodal"><i class="bi bi-trash-fill"></i></button></td>
                             </tr>`;
            })
            tablebody.innerHTML = opciones

            const botonesAbrirModal = document.querySelectorAll('.btn-eliminar');
            botonesAbrirModal.forEach(boton => {
                boton.addEventListener('click', async () => {
                    const materiaId = boton.getAttribute('data-materia-id');
                    // Al abrir el modal, establecer el ID de materia a eliminar en el campo oculto dentro del modal
                    document.getElementById('input-materia-id').value = materiaId;
                    console.log(materiaId);
                });
            });

        } else if (data.message === "No hay datos") {
            let opciones = ``;
            opciones += `<tr>
                             </tr>`;
            tablebody.innerHTML = opciones
        } else {
            alert("No hay datos")
        }
    } catch (error) {
        console.log(error);
    }
}

mostrarTablaEventos = async () => {
    try {
        const response = await fetch("tabla_eventos/",{
            method: 'GET',
            headers: {
                'Authorization': 'Bearer my_secret_token'
            }
        });
        const datas = await response.json();
        console.log(datas);

        if (datas.message === "Success") {

            let opciones = ``;
            datas.datos.forEach((dato) => {
                opciones += `<tr>
                             <td class="campo-evento">${dato.Evento}</td>
                             <td class="text-center">${dato.Fecha_actividad}</td>
                             <td class="text-center">${dato.Sala}</td>
                             <td class="text-center">
                                <button type="button" class="btn btn-danger btn-eliminarevento" 
                                        data-evento-id="${dato.id}" data-bs-toggle="modal" 
                                        data-bs-target="#eliminarevento">
                                        <i class="bi bi-trash-fill"></i></button>
                                <button type="button" class="btn btn-primary btn-editarevento"
                                        data-eventoedit-id="${dato.id}"
                                        data-bs-toggle="modal" data-bs-target="#editarEventoModal"><i
                                        class="bi bi-pencil-square"></i></button>
                             </td>
                             </tr>`;
            })

            tableeventos.innerHTML = opciones

            const botonesEditarEvento = document.querySelectorAll('.btn-editarevento');
            botonesEditarEvento.forEach(boton => {
                boton.addEventListener('click', async () => {
                    const eventoidedit = boton.getAttribute('data-eventoedit-id');
                    // Llamar a función para obtener y prellenar datos del evento en el modal
                    await obtenerYMostrarDatosEvento(eventoidedit);
                });
            });
            const botonesAbrirModal = document.querySelectorAll('.btn-eliminarevento');
            botonesAbrirModal.forEach(boton => {
                boton.addEventListener('click', async () => {
                    const eventoId = boton.getAttribute('data-evento-id');
                    // Al abrir el modal, establecer el ID de materia a eliminar en el campo oculto dentro del modal
                    document.getElementById('input-evento-id').value = eventoId;
                    console.log(eventoId);
                });
            });

        } else if (data.message === "No hay datos") {
            let opciones = ``;
            opciones += `<tr>
                             </tr>`;
            tableeventos.innerHTML = opciones
        } else {
            //alert("No hay datos")
        }
    } catch (error) {
        console.log(error);
    }
}
const obtenerYMostrarDatosEvento = async (eventoidedit) => {
    try {
        const response = await fetch(`obtener_evento/${eventoidedit}/`,{
            method: 'GET',
            headers: {
                'Authorization': 'Bearer my_secret_token'
            }
        });
        const data = await response.json();
        console.log(data)

        if (data.message === 'Success') {
            const evento = data.evento;

            // Preencher el modal de editar con los datos obtenidos
            document.getElementById('evento-id-editar').value = evento.id
            document.getElementById('inputEventoEdit').value = evento.nombre_evento;
            document.getElementById('salasEditar').value = evento.sala_id.toString();
            document.getElementById('datetimefechaEdit').querySelector('input').value = evento.fecha_actividad;
            document.getElementById('datetimenotificacionEdit').querySelector('input').value = evento.fecha_notificacion;

            // Aquí puedes añadir más campos del formulario según sea necesario
        } else {
            alert('Error al obtener datos del evento');
        }
    } catch (error) {
        console.error('Error al obtener datos del evento:', error);
    }
}

const cargaInicial = async () => {
    const idCarreraInicial = 1; // Valor predeterminado para idCarrera
    const semestreInicial = 1; // Valor predeterminado para Semestre

    await listarCarreras();
    await mostrarsemestre();
    await mostrarTabla();
    await listarsalas();
    await listarsalasedit();
    await mostrarTablaEventos();
    await listarNotificaciones();

    await listarMaterias(idCarreraInicial, semestreInicial); // Llamar a listarMaterias con valores iniciales

    carrera.addEventListener("change", async (event) => {
        const idCarreraSeleccionada = event.target.value;
        const semestreSeleccionado = semestre.value;
        await listarMaterias(idCarreraSeleccionada, semestreSeleccionado);
    })

    semestre.addEventListener("change", async (event) => {
        const idCarreraSeleccionada = carrera.value;
        const semestreSeleccionado = event.target.value;
        await listarMaterias(idCarreraSeleccionada, semestreSeleccionado);

    })

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Busca la cookie con el nombre 'csrftoken'
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    document.getElementById('btnguar').addEventListener('click', async function () {
        const checkboxess = document.querySelectorAll('input[name="materias"]:checked');
        const materiasSeleccionadas = Array.from(checkboxess).map(checkbox => checkbox.value);
        console.log(materiasSeleccionadas)
        console.log(csrftoken)

        try {
            const response = await fetch('guardar_materias/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({materia_id: materiasSeleccionadas})
            });

            if (!response.ok) {
                throw new Error('Hubo un problema al guardar las materias.');
            }

            const data = await response.json();
            console.log('Materias guardadas correctamente:', data);
            // Desmarcar todos los checkboxes
            checkboxess.forEach(checkbox => {
                checkbox.checked = false;
            });


            document.getElementById('error-container').textContent = '';

            // Llamar a mostrarTabla() para actualizar la tabla en tiempo real
            await mostrarTabla();

        } catch (error) {
            console.error('Error al guardar las materias:', error);
            showErrorMessage('Materia Existente.');
            // Ocultar el mensaje de error después de 3 segundos
            setTimeout(hideErrorMessage, 5000);
        }
    });

    const checkboxes = document.querySelectorAll('input[name="materias"]');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function (event) {
            if (this.checked) {
                const valorCheckbox = this.value;
                console.log("El valor del checkbox es:", valorCheckbox);
            } else {
                console.log("El checkbox ha sido desmarcado");
            }
        });
    });

    document.getElementById('btn-confirmar-eliminacionevento').addEventListener('click', async () => {
        try {
            // Obtener el ID de la materia a eliminar del campo oculto en el modal
            const evento_id = document.getElementById('input-evento-id').value;
            console.log(evento_id)

            // Realizar la solicitud para eliminar la materia
            const response = await fetch(`eliminar_evento/${evento_id}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                }
            });

            // Verificar si la eliminación fue exitosa
            if (response.ok) {
                console.log('Evento eliminado correctamente');
                // Actualizar la tabla o realizar cualquier otra acción necesaria después de la eliminación
                await mostrarTablaEventos();
                // Cerrar el modal después de eliminar la materia
                $('#eliminarevento').modal('hide');
                $('#modaleventos').modal('show');
            } else {
                console.error('Error al eliminar el evento');
                // Mostrar un mensaje de error u otra acción de manejo de errores si es necesario
            }
        } catch (error) {
            console.error('Error al eliminar el evento:', error);
            // Mostrar un mensaje de error u otra acción de manejo de errores si es necesario
        }
    });

    document.getElementById('btn-confirmar-eliminacion').addEventListener('click', async () => {
        try {
            // Obtener el ID de la materia a eliminar del campo oculto en el modal
            const relacion_id = document.getElementById('input-materia-id').value;
            console.log(relacion_id)

            // Realizar la solicitud para eliminar la materia
            const response = await fetch(`eliminar_relacion/${relacion_id}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                }
            });

            // Verificar si la eliminación fue exitosa
            if (response.ok) {
                console.log('Materia eliminada correctamente');
                // Actualizar la tabla o realizar cualquier otra acción necesaria después de la eliminación
                await mostrarTabla();
                // Cerrar el modal después de eliminar la materia
                $('#eliminarmodal').modal('hide');
                $('#modalmaterias').modal('show');
            } else {
                console.error('Error al eliminar la materia');
                // Mostrar un mensaje de error u otra acción de manejo de errores si es necesario
            }
        } catch (error) {
            console.error('Error al eliminar la materia:', error);
            // Mostrar un mensaje de error u otra acción de manejo de errores si es necesario
        }
    });

    document.getElementById('btn-agregarevento').addEventListener('click', async function () {
        const nombreEvento = document.getElementById('inputEvento').value;
        const sala = document.getElementById('salas').value;
        const fechaActividad = document.getElementById('datetimefecha').querySelector('input').value;
        const fechaNotificacion = document.getElementById('datetimenotificacion').querySelector('input').value;

        const fechaActividadDt = new Date(fechaActividad);
        const fechaNotificacionDt = new Date(fechaNotificacion);

        if (fechaNotificacionDt > fechaActividadDt) {
            // Mostrar el toast
            const toastEl = document.getElementById('liveToast');
            const toast = new bootstrap.Toast(toastEl);
            toast.show();
            return;
        }
        const data = {
            nombre_evento: nombreEvento,
            sala: sala,
            fecha_actividad: fechaActividad,
            fecha_notificacion: fechaNotificacion,
        };
        console.log(data)
        try {
            const response = await fetch('guardar_evento/', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                }
            });

            if (!response.ok) {
                throw new Error('Hubo un problema al guardar el evento.');
            }

            const responseData = await response.json();
            if (responseData.message === 'Success') {
                // Acción cuando se guarda correctamente
                // Recargar la página o actualizar la lista de eventos
                await mostrarTablaEventos()
                $('#agregarevento').modal('hide');
                $('#modaleventos').modal('show');
            } else {
                // Manejo de errores
                if (responseData.message === 'La fecha de notificación no puede ser posterior a la fecha del evento.') {
                    const toastEl = document.getElementById('liveToast');
                    const toast = new bootstrap.Toast(toastEl);
                    toast.show();
                }
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al guardar el evento');
        }
    });
    document.getElementById('btn-editarEvento').addEventListener('click', async function () {
        const eventoId = document.getElementById('evento-id-editar').value;
        const nombreEvento = document.getElementById('inputEventoEdit').value;
        const sala = document.getElementById('salasEditar').value;
        const fechaActividad = document.getElementById('datetimefechaEdit').querySelector('input').value;
        const fechaNotificacion = document.getElementById('datetimenotificacionEdit').querySelector('input').value;

        const fechaActividadDt = new Date(fechaActividad);
        const fechaNotificacionDt = new Date(fechaNotificacion);

        if (fechaNotificacionDt > fechaActividadDt) {
            const toastEl = document.getElementById('liveToast');
            const toast = new bootstrap.Toast(toastEl);
            toast.show();
            return;
        }

        const data = {
            id: eventoId,
            nombre_evento: nombreEvento,
            sala: sala,
            fecha_actividad: fechaActividad,
            fecha_notificacion: fechaNotificacion,
        };

        try {
            const response = await fetch('editar_evento/', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken  // Asegúrate de que tienes el token CSRF en tu plantilla
                }
            });

            if (response.ok) {
                const result = await response.json();
                if (result.message === 'Success') {
                    await mostrarTablaEventos()
                    $('#editarEventoModal').modal('hide');
                    $('#modaleventos').modal('show');

                } else {
                    if (result.message === 'La fecha de notificación no puede ser posterior a la fecha del evento.') {
                        const toastEl = document.getElementById('liveToast');
                        const toast = new bootstrap.Toast(toastEl);
                        toast.show();
                    }
                }
            } else {
                throw new Error('Error al actualizar el evento');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al actualizar el evento');
        }
    });
document.getElementById('btnvisto').addEventListener('click', async function() {
    try {
        const response = await fetch("notificaciones/", {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer my_secret_token'
            }
        });

        if (!response.ok) {
            throw new Error('Error en la solicitud de notificaciones');
        }

        const data = await response.json();
        console.log("Datos obtenidos:", data);

         if (data.message === "Not Found") {
            console.log('Notificaciones no encontradas, proceso abortado.');
            return;  // Salir de la función si el mensaje es "Not Found"
        }
        const promises = data.notificaciones.map(async (notificacion) => {
            if (notificacion.id) {
                const requestData = { id: notificacion.id };
                const postResponse = await fetch('marcar_visto/', {
                    method: 'POST',
                    body: JSON.stringify(requestData),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    }
                });

                if (!postResponse.ok) {
                    const errorData = await postResponse.json();
                    console.error('Error en la respuesta:', errorData);
                    alert('Error en la respuesta del servidor');
                } else {
                    const result = await postResponse.json();
                    if (result.message !== 'Evento marcado como visto correctamente') {
                        alert(result.message);
                    }
                }
            }
        });

        await Promise.all(promises);
        console.log('Todas las notificaciones marcadas como vistas');
        listarNotificaciones();
    } catch (error) {
        console.error('Error:', error);
        alert('Error al actualizar las notificaciones');
    }
});



};

function showErrorMessage(message) {
    const errorContainer = document.getElementById('error-container');
    errorContainer.textContent = message;
    errorContainer.style.display = 'block'; // Mostrar el mensaje de error
}

function hideErrorMessage() {
    const errorContainer = document.getElementById('error-container');
    errorContainer.style.display = 'none'; // Ocultar el mensaje de error
}

window.addEventListener("load", async () => {
    await cargaInicial();

});

const formatDate = (isoDate) => {
    const date = new Date(isoDate);
    const optionsDate = {
        day: 'numeric',
        month: 'long'
    };
    const optionsTime = {
        hour: 'numeric',
        minute: 'numeric'
    };
    const formattedDate = date.toLocaleDateString('es-ES', optionsDate);
    const formattedTime = date.toLocaleTimeString('es-ES', optionsTime);
    return `${formattedDate}, ${formattedTime}`;
};
const calculateDaysDifference = (futureDate) => {
    const oneDay = 24 * 60 * 60 * 1000; // horas * minutos * segundos * milisegundos
    const currentDate = new Date();
    const targetDate = new Date(futureDate);
    const diffDays = Math.round((targetDate - currentDate) / oneDay);
    return diffDays;
};
const calculateHoursDifference = (futureDate) => {
    const oneHour = 60 * 60 * 1000; // minutos * segundos * milisegundos
    const oneMinute = 60 * 1000; // segundos * milisegundos
    const oneSecond = 1000; // milisegundos
    const currentDate = new Date();
    const targetDate = new Date(futureDate);
    const diffMilliseconds = targetDate - currentDate;

    const diffHours = diffMilliseconds / oneHour;

    if (Math.abs(diffHours) >= 1) {
        return `${Math.round(diffHours)} horas`;
    } else if (Math.abs(diffMilliseconds) >= oneMinute) {
        const diffMinutes = diffMilliseconds / oneMinute;
        if(diffMinutes>1){
            return `${Math.round(diffMinutes)} minutos`;
        }else{
            return `${Math.round(diffMinutes)} minuto`;
        }

    }
};
