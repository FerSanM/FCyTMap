import os

import pytz
from django.db import connection
from django.views.decorators.http import require_http_methods

from .models import User, Carrera, Actividades
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import User, Carrera, Sala
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import render
from .models import Materia
from django.shortcuts import render, redirect
from .models import RelacionUsuarioMateria
from django.shortcuts import render
from .models import User, Materia
import json
import datetime
from django.views.decorators.csrf import csrf_protect
from .models import RelacionUsuarioMateria, RelacionMateriaSala
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render

GOOGLE_OAUTH_CLIENT_ID = "425881363668-uga1n538hfcmijovqjbu70hnpmne6ij4.apps.googleusercontent.com"

def sign_in(request):
    return render(request, 'sign_in.html')

def custom_logout(request):
    logout(request)
    return redirect('login')
def inicio(request):
    usuario = request.user
    ubicaciones = Sala.objects.all()

    if usuario.is_authenticated:
        userdata = SocialAccount.objects.filter(user_id=usuario.id)
    else:
        return redirect('login')
    # Obtener el día de la semana actual (lunes=0, martes=1, ..., domingo=6)
    dia_actual = datetime.datetime.now().weekday()
    dia_actual = dia_actual + 1
    hora_actual = datetime.datetime.now().time()
    relaciones_sala_materia = RelacionMateriaSala.objects.filter(dia_semana=dia_actual, hora_entrada__lte=hora_actual,
                                                                 hora_salida__gte=hora_actual)

    iduser = request.user.id
    materias_seleccionadas = Materia.objects.filter(relacionusuariomateria__usuario__id=iduser)
    actividades_usuario = Actividades.objects.filter()
    # Consulta utilizando el ORM de Django
    ids_materias_relacionadas = [relacion.materia_id for relacion in relaciones_sala_materia]
    # print("Los ID de materia",ids_materias_relacionadas)
    materias_filtradas = materias_seleccionadas.filter(id__in=ids_materias_relacionadas)

    ahora = timezone.localtime(timezone.now())
    inicio_hoy = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_hoy = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)

    eventos = Actividades.objects.filter(
        idUsuario=iduser,
        fecha_actividad__lte=ahora,
        fecha_actividad__range=(inicio_hoy, fin_hoy))

    return render(request, 'inicio.html', {
        'ubicaciones': ubicaciones,
        'relaciones': relaciones_sala_materia,
        'materias_usuario': materias_filtradas,
        'userdata': userdata,
        'eventos': eventos
    })


def iniciosin(request):
    ubicaciones = Sala.objects.all()

    # Obtener el día de la semana actual (lunes=0, martes=1, ..., domingo=6)
    dia_actual = datetime.datetime.now().weekday()
    dia_actual = dia_actual + 1
    hora_actual = datetime.datetime.now().time()
    relaciones_sala_materia = RelacionMateriaSala.objects.filter(dia_semana=dia_actual, hora_entrada__lte=hora_actual,
                                                                 hora_salida__gte=hora_actual)

    return render(request, 'iniciosin.html', {
        'ubicaciones': ubicaciones,
        'relaciones': relaciones_sala_materia,
    })


@csrf_exempt
def auth_receiver(request):
    token = request.POST.get('credential')

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), GOOGLE_OAUTH_CLIENT_ID
        )
    except ValueError:
        # Si el token no es válido, retorna una respuesta HTTP con el estado 403 (Forbidden)
        return HttpResponse(status=403)
    except Exception as e:
        # Captura cualquier otra excepción y maneja el error de manera adecuada
        # Puedes imprimir el error para depuración o registrar el error en tu sistema de registro
        print(f"Ocurrió un error durante la verificación del token: {e}")
        return HttpResponse(status=500)

    # Si la verificación del token fue exitosa, almacena los datos del usuario en la sesión y redirige
    request.session['user_data'] = user_data

    correo_electronico = user_data.get('email')
    print(correo_electronico)
    if User.objects.filter(correo_electronico=correo_electronico).exists():
        print("cuenta ya existente")
        pass
    else:
        nombre = user_data.get('given_name')
        apellido = user_data.get('family_name')
        nuevo_usuario = User(nombre=nombre, apellido=apellido, correo_electronico=correo_electronico)
        nuevo_usuario.save()
    return redirect('inicio', )


def sign_out(request):
    del request.session['user_data']
    print("Sesion Cerrada")
    return redirect('sign_in')


def login(request):
    return render(request, 'login.html')


"""
select de materias sin filtro
def mostrar_materias(request):
    materias = Materia.objects.all()
    return render(request, 'mostrar_materias.html', {'materias': materias})
"""
"""
select de materias segun semestre
def mostrar_materias(request):
    semestre_seleccionado = request.GET.get('semestre', 1)  # Obtener el semestre seleccionado, por defecto será 1
    materias = Materia.objects.filter(Semestre=semestre_seleccionado)
    return render(request, 'mostrar_materias.html',{'materias': materias, 'semestre_seleccionado': semestre_seleccionado})
"""


# Select con filtro de carrera y semestre


def mostrar_materias(request):
    return render(request, 'mostrar_materias')


"""def mostrar_materias(request):
    semestre_seleccionado = request.GET.get('semestre', 1)
    carrera_seleccionada = request.GET.get('carrera', 1)  # Seleccionar por defecto la carrera con ID 1
    materias = Materia.objects.filter(semestre=semestre_seleccionado, idCarrera=carrera_seleccionada)
    carreras = Carrera.objects.all()


    # Obtener el correo electrónico del usuario de la sesión
    correo_usuario = request.session.get('user_data', {}).get('email')

    print("Este es el correo del incio de Sesion", correo_usuario)

    #print("Este es el correo del incio de Sesion",correo_usuario)
    # Buscar el usuario en la base de datos usando el correo electrónico
    usuario = User.objects.filter(correo_electronico=correo_usuario).first()
    iduser = usuario.id
    materias_seleccionadas = Materia.objects.filter(relacionusuariomateria__usuario__id=iduser)
    #print("MATERIAS SELECCIONADAS",materias_seleccionadas)
    return render(request, 'mostrar_materias.html', {
        'usuario': usuario,
        'materias': materias,
        'semestre_seleccionado': semestre_seleccionado,
        'carrera_seleccionada': carrera_seleccionada,
        'carreras': carreras
    })"""

from django.http import HttpResponseRedirect
from django.urls import reverse


@csrf_exempt
def guardar_materias(request):
    iduser = request.user.id
    print("Usuari")
    if request.method == 'POST':
        data = json.loads(request.body)
        materias_seleccionadas = data.get('materia_id', [])

        if RelacionUsuarioMateria.objects.filter(usuario_id=iduser, materia_id__in=materias_seleccionadas).exists():
            return JsonResponse({'message': 'No se pueden guardar materias repetidas.'}, status=400)

        for materia_id in materias_seleccionadas:
            relacion = RelacionUsuarioMateria(usuario_id=iduser, materia_id=materia_id)
            relacion.save()
            print("jjajajajajajajajajajajja")
        return JsonResponse({'message': 'Materias guardadas correctamente'})
    else:
        return JsonResponse({'error': 'No se pudo procesar la solicitud'}, status=400)


@csrf_exempt
def guardar_evento(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print('Datos recibidos:', data)
        nombre_evento = data.get('nombre_evento')
        sala_id = data.get('sala')
        fecha_actividad = data.get('fecha_actividad')
        fecha_notificacion = data.get('fecha_notificacion')

        if nombre_evento and sala_id and fecha_actividad and fecha_notificacion:
            try:
                sala = Sala.objects.get(id=sala_id)
                formato_fecha = '%d/%m/%Y %H:%M'
                fecha_actividad_dt = datetime.datetime.strptime(fecha_actividad, formato_fecha)
                fecha_notificacion_dt = datetime.datetime.strptime(fecha_notificacion, formato_fecha)
                if fecha_notificacion_dt > fecha_actividad_dt:
                    return JsonResponse(
                        {'message': 'La fecha de notificación no puede ser posterior a la fecha del evento.'})

                # Convert to aware datetime with timezone information
                timezone_asuncion = pytz.timezone('America/Asuncion')  # Adjust timezone as needed
                fecha_actividad_aware = timezone_asuncion.localize(fecha_actividad_dt)
                fecha_notificacion_aware = timezone_asuncion.localize(fecha_notificacion_dt)

                evento = Actividades(
                    descripcion=nombre_evento,
                    idSala=sala,
                    fecha_actividad=fecha_actividad_aware,
                    fecha_notificacion=fecha_notificacion_aware,
                    idUsuario=request.user
                )
                evento.save()
                return JsonResponse({'message': 'Success'})
            except ValueError as e:
                return JsonResponse({'message': f'Error de formato de fecha: {str(e)}'}, status=400)
            except Sala.DoesNotExist:
                return JsonResponse({'message': 'Sala no encontrada'}, status=400)
        else:
            return JsonResponse({'message': 'Datos incompletos'}, status=400)
    return JsonResponse({'message': 'Método no permitido'}, status=405)


def eliminar_materias(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        materia_id = request.POST.get('materia_id')

        if materia_id:
            try:
                relacion_materia_usuario = RelacionUsuarioMateria.objects.get(materia=materia_id, usuario=usuario_id)
                relacion_materia_usuario.delete()
                print("Materia Eliminada :D")
                return redirect('mostrar_materias')
            except RelacionUsuarioMateria.DoesNotExist:
                return redirect('mostrar_materias')


def get_carreras(request):
    carreras = list(Carrera.objects.values())

    if len(carreras) > 0:
        data = {'message': "Success", 'carreras': carreras}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)


def get_materias(request, idcarrera, semestre):
    materias = list(Materia.objects.filter(idCarrera=idcarrera, semestre=semestre).values())

    if len(materias) > 0:
        data = {'message': "Success", 'materias': materias}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)


@require_http_methods(["DELETE"])
def eliminar_relacion(request, relacion_id):
    try:
        # Buscar la relación por su ID
        relacion_eliminar = RelacionUsuarioMateria.objects.get(id=relacion_id)
        # Eliminar la relación
        relacion_eliminar.delete()
        # Devolver una respuesta de éxito
        return JsonResponse({'message': 'Relación eliminada correctamente'})
    except RelacionUsuarioMateria.DoesNotExist:
        # Si la relación no existe, devolver un error
        return JsonResponse({'error': 'La relación especificada no existe'}, status=404)
    except Exception as e:
        # Si ocurre algún otro error, devolver un error genérico
        return JsonResponse({'error': 'Hubo un problema al eliminar la relación'}, status=500)


@require_http_methods(["DELETE"])
def eliminar_evento(request, evento_id):
    try:
        # Buscar la relación por su ID
        evento_eliminar = Actividades.objects.get(id=evento_id)
        # Eliminar la relación
        evento_eliminar.delete()
        # Devolver una respuesta de éxito
        return JsonResponse({'message': 'Evento eliminada correctamente'})
    except RelacionUsuarioMateria.DoesNotExist:
        # Si la relación no existe, devolver un error
        return JsonResponse({'error': 'El evento especificado no existe'}, status=404)
    except Exception as e:
        # Si ocurre algún otro error, devolver un error genérico
        return JsonResponse({'error': 'Hubo un problema al eliminar el evento'}, status=500)


def get_tabla(request):
    usuario = request.user
    if usuario:
        id_usuario = usuario.id
        relaciones_usuario_materia = RelacionUsuarioMateria.objects.filter(usuario_id=id_usuario)

        if relaciones_usuario_materia:
            datos = []

            for relacion in relaciones_usuario_materia:
                materia_id = relacion.materia_id
                materia = Materia.objects.filter(id=materia_id).first()

                if materia:
                    # Aquí puedes agregar los campos de la tabla Materia que necesites
                    datos.append({
                        'id': relacion.id,
                        'Materia': materia.descripcion,
                        'Semestre': materia.semestre
                    })
            if datos:
                return JsonResponse({'message': 'Success', 'datos': datos})
            else:
                return JsonResponse({'message': 'No se encontraron datos de la materia para el usuario'})
        else:
            return JsonResponse({'message': 'No hay datos'})
    else:
        return JsonResponse({'message': 'Usuario no encontrado'})


def get_tablaeventos(request):
    usuario = request.user
    if usuario:
        id_usuario = usuario.id
        eventos = Actividades.objects.filter(idUsuario_id=id_usuario)
        if eventos:
            datos = []
            for evento in eventos:
                sala_id = evento.idSala_id
                sala = Sala.objects.filter(id=sala_id).first()

                if sala:
                    datos.append({
                        'id': evento.id,
                        'Sala': sala.descripcion,
                        'Evento': evento.descripcion,
                        'Fecha_actividad': evento.fecha_actividad.strftime('%d/%m/%Y %H:%M'),
                    })
            if datos:
                return JsonResponse({'message': 'Success', 'datos': datos})
            else:
                return JsonResponse({'message': 'No hay datos'})
        else:
            return JsonResponse({'message': 'No encontraron datos de Evento'})
    else:
        return JsonResponse({'message': 'Usuario no encontrado'})


def get_notificaciones(request):
    usuario = request.user
    if usuario:
        id_usuario = usuario.id
        print(id_usuario)

        ahora = timezone.localtime(timezone.now())
        print(ahora)
        inicio_hoy = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
        print(inicio_hoy)
        fin_hoy = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)
        print(fin_hoy)

        notificaciones = list(Actividades.objects.filter(
            idUsuario=id_usuario,
            fecha_notificacion__lte=ahora,

        ).order_by('-fecha_actividad').values())

        if len(notificaciones) > 0:
            data = {'message': "Success", 'notificaciones': notificaciones}
        else:
            data = {'message': "Not Found"}

        return JsonResponse(data)


def get_sala(request):
    salas = list(Sala.objects.values())

    if len(salas) > 0:
        sala = {'message': "Success", 'salas': salas}
    else:
        sala = {'message': "Not Found"}

    return JsonResponse(sala)


def get_actividades(request):
    usuario = request.user
    if usuario:
        id_usuario = usuario.id

        ahora = timezone.localtime(timezone.now())
        print(ahora)
        inicio_hoy = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
        print(inicio_hoy)
        fin_hoy = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)
        print(fin_hoy)

        notificaciones = list(Actividades.objects.filter(
            idUsuario=id_usuario,
            fecha_actividad__lte=ahora,
            fecha_actividad__range=(inicio_hoy, fin_hoy)
        ).select_related('idSala').values(
            'id', 'descripcion', 'fecha_actividad', 'fecha_notificacion', 'idSala__nombre', 'idSala__ubicacion'
        ))

        if len(notificaciones) > 0:
            data = {'message': "Success", 'notificaciones': notificaciones}
        else:
            data = {'message': "Not Found"}

        return JsonResponse(data)


def obtener_evento(request, evento_id):
    try:
        evento = get_object_or_404(Actividades, id=evento_id)

        # Preparar los datos del evento para enviar como respuesta JSON
        data = {
            'message': 'Success',
            'evento': {
                'id': evento.id,
                'nombre_evento': evento.descripcion,  # Ajusta según el nombre del campo en tu modelo
                'sala_id': evento.idSala_id,  # Ajusta según el nombre del campo en tu modelo y relación de sala
                'fecha_actividad': evento.fecha_actividad.strftime('%d/%m/%Y %H:%M'),  # Formato de fecha
                'fecha_notificacion': evento.fecha_notificacion.strftime('%d/%m/%Y %H:%M'),  # Formato de fecha
                # Agrega más campos según sea necesario
            }
        }

        return JsonResponse(data)

    except Actividades.DoesNotExist:
        return JsonResponse({'message': 'Evento no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


@csrf_exempt
def editar_evento(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        evento_id = data.get('id')
        nombre_evento = data.get('nombre_evento')
        sala_id = data.get('sala')
        fecha_actividad = data.get('fecha_actividad')
        fecha_notificacion = data.get('fecha_notificacion')

        if evento_id and nombre_evento and sala_id and fecha_actividad and fecha_notificacion:
            try:
                evento = Actividades.objects.get(id=evento_id)
                salas = Sala.objects.get(id=sala_id)
                fecha_actividad_dta = datetime.datetime.strptime(fecha_actividad, '%d/%m/%Y %H:%M')
                fecha_notificacion_dta = datetime.datetime.strptime(fecha_notificacion, '%d/%m/%Y %H:%M')

                if fecha_notificacion_dta > fecha_actividad_dta:
                    return JsonResponse(
                        {'message': 'La fecha de notificación no puede ser posterior a la fecha del evento.'})
                timezones = pytz.timezone('America/Asuncion')
                fecha_actividad_aware = timezones.localize(fecha_actividad_dta)
                fecha_notificacion_aware = timezones.localize(fecha_notificacion_dta)

                evento.descripcion = nombre_evento
                evento.idSala = salas
                evento.fecha_actividad = fecha_actividad_aware
                evento.fecha_notificacion = fecha_notificacion_aware
                evento.save()

                return JsonResponse({'message': 'Success'})
            except Actividades.DoesNotExist:
                return JsonResponse({'message': 'Evento no encontrado'}, status=400)
            except Sala.DoesNotExist:
                return JsonResponse({'message': 'Sala no encontrada'}, status=400)
            except ValueError as e:
                return JsonResponse({'message': f'Error de formato de fecha: {str(e)}'}, status=400)
        else:
            return JsonResponse({'message': 'Datos incompletos'}, status=400)
    return JsonResponse({'message': 'Método no permitido'}, status=405)
