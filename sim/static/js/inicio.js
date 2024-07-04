const listarMaterias = async (idCarrera, Semestre) => {
    try {
        const response = await fetch(`materias/${idCarrera}/${Semestre}`);
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
        const response = await fetch("notificaciones/");
        const data = await response.json();
        console.log(data);

        if (data.message === "Success") {
            let opciones = ``;
            data.notificaciones.forEach((notificacion) => {
                const fechaFormateada = formatDate(notificacion.fecha_actividad);
                const diasFaltantes = calculateDaysDifference(notificacion.fecha_actividad);
                let mensajeDias = '';
                if (new Date() >= new Date(notificacion.fecha_actividad)) {
                    mensajeDias = 'Finalizado';
                } else {
                    mensajeDias = `Faltan ${diasFaltantes} días para el evento`;
                }
                opciones += `
                    <li class="li-noti">
                        <a class="dropdown-item" href="#">
                            <div class="noti-container">
                                <div class="icon-noti">
                                    <i class="bi bi-journal-bookmark-fill"></i>
                                </div>
                                <div class="content-noti">
                                    <span style="font-size: 12px">Notificacion de Evento</span><br>
                                    <span><b>${notificacion.descripcion}</b></span><br>
                                     <span style="font-size: 12px">${mensajeDias}</span>
                                </div>
                            </div>
                        </a>
                    </li>`;
            });

            // Agregar el último <li> al final
            opciones += `
                <li>
                    <footer class="footer-noti">
                        <a href="#">Ver Más</a>
                    </footer>
                </li>`;

            document.getElementById('notif').innerHTML = opciones;

        } else {
            alert("Datos no encontrados");
        }
    } catch (error) {
        console.log(error);
    }
};

const listarCarreras = async () => {
    try {
        const response = await fetch("carreras/");
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
        const response = await fetch("tabla/");
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
document.addEventListener('DOMContentLoaded', async () => {
    // Agregar evento de clic para abrir el modal de confirmación
    const botonesAbrirModal = document.querySelectorAll('.btn-eliminar');
    botonesAbrirModal.forEach(boton => {
        boton.addEventListener('click', async () => {
            const materiaId = boton.getAttribute('data-materia-id');
            // Al abrir el modal, establecer el ID de materia a eliminar en el campo oculto dentro del modal
            document.getElementById('input-materia-id').value = materiaId;
            console.log(materiaId);
        });
    });

    // Aquí puedes colocar otros códigos relacionados con el DOM
});


const cargaInicial = async () => {
    const idCarreraInicial = 1; // Valor predeterminado para idCarrera
    const semestreInicial = 1; // Valor predeterminado para Semestre

    await listarCarreras();
    await mostrarsemestre();
    await mostrarTabla();
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

    // Asociar evento de clic al botón "Eliminar" en el modal
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