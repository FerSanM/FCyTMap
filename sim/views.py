import os

from django.views.decorators.http import require_http_methods

from .models import User, Carrera
from django.http import HttpResponse, JsonResponse

from .models import User, Carrera, Sala
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import render
from .models import Materia
import jwt
from django.shortcuts import render, redirect
from .models import RelacionUsuarioMateria
from django.shortcuts import render
from .models import User, Materia
import json
from django.views.decorators.csrf import csrf_protect
import datetime
from .models import RelacionUsuarioMateria, RelacionMateriaSala

GOOGLE_OAUTH_CLIENT_ID = "425881363668-ch0d9plss8pnoukc95a22rpdj54bgaot.apps.googleusercontent.com"


def sign_in(request):
    return render(request, 'sign_in.html')


def inicio(request):
    # semestre_seleccionado = request.GET.get('semestre', 1)
    # carrera_seleccionada = request.GET.get('carrera', 1)  # Seleccionar por defecto la carrera con ID 1
    # materias = Materia.objects.filter(Semestre=semestre_seleccionado, idCarrera=carrera_seleccionada)
    # carreras = Carrera.objects.all()

    # Obtener el correo electrónico del usuario de la sesión
    correo_usuario = request.session.get('user_data', {}).get('email')
    print("Este es el correo del incio de Sesion", correo_usuario)
    # Buscar el usuario en la base de datos usando el correo electrónico
    usuario = User.objects.filter(correo_electronico=correo_usuario).first()
    iduser = usuario.id
    print("id del Usuario :", iduser)
    ubicaciones = Sala.objects.all()

    # Obtener el día de la semana actual (lunes=0, martes=1, ..., domingo=6)
    dia_actual = datetime.datetime.now().weekday()
    dia_actual = dia_actual + 1
    hora_actual = datetime.datetime.now().time()
    relaciones_sala_materia = RelacionMateriaSala.objects.filter(dia_semana=dia_actual, hora_entrada__lte=hora_actual,
                                                                 hora_salida__gte=hora_actual)
    correo_usuario = request.session.get('user_data', {}).get('email')
    usuario = User.objects.filter(correo_electronico=correo_usuario).first()

    # print(relaciones_sala_materia)
    # print("Total de datos en ubicaciones:", len(ubicaciones))
    # print("Total de datos en relaciones:",len(relaciones_sala_materia))
    # print("Seleccion del usuario :",materias_seleccionadas)
    return render(request, 'inicio.html', {
        'ubicaciones': ubicaciones,
        'relaciones': relaciones_sala_materia,

    })


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
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
    correo_usuario = request.session.get('user_data', {}).get('email')
    usuario = User.objects.filter(correo_electronico=correo_usuario).first()
    iduser = usuario.id

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
    materias = list(Materia.objects.filter(idCarrera=idcarrera, Semestre=semestre).values())

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


def get_tabla(request):
    correo_usuario = request.session.get('user_data', {}).get('email')
    usuario = User.objects.filter(correo_electronico=correo_usuario).first()

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
                        'Materia': materia.Descripcion,
                        'Semestre': materia.Semestre
                    })
            if datos:
                return JsonResponse({'message': 'Success', 'datos': datos})
            else:
                return JsonResponse({'message': 'No se encontraron datos de la materia para el usuario'})
        else:
            return JsonResponse({'message': 'No se encontraron relaciones usuario-materia para el usuario'})
    else:
        return JsonResponse({'message': 'Usuario no encontrado'})
