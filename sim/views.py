import os
from .models import User, Carrera,Sala
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
GOOGLE_OAUTH_CLIENT_ID = "425881363668-ch0d9plss8pnoukc95a22rpdj54bgaot.apps.googleusercontent.com"


def sign_in(request):
    return render(request, 'sign_in.html')


def inicio(request):
    ubicaciones = Sala.objects.all()
    return render(request, 'inicio.html',{'ubicaciones': ubicaciones})


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
    return redirect('inicio',)

def sign_out(request):
    del request.session['user_data']
    print("Sesion Cerrada")
    return redirect('sign_in')




#Select con filtro de carrera y semestre
from django.shortcuts import render
from .models import User, Materia

def mostrar_materias(request):
    semestre_seleccionado = request.GET.get('semestre', 1)
    carrera_seleccionada = request.GET.get('carrera', 1)  # Seleccionar por defecto la carrera con ID 1
    materias = Materia.objects.filter(semestre=semestre_seleccionado, idCarrera=carrera_seleccionada)
    carreras = Carrera.objects.all()


    # Obtener el correo electrónico del usuario de la sesión
    correo_usuario = request.session.get('user_data', {}).get('email')
    #print("Este es el correo del incio de Sesion",correo_usuario)
    # Buscar el usuario en la base de datos usando el correo electrónico
    usuario = User.objects.filter(correo_electronico=correo_usuario).first()
    iduser = usuario.id
    materias_seleccionadas = Materia.objects.filter(relacionusuariomateria__usuario__id=iduser)
    print("MATERIAS SELECCIONADAS",materias_seleccionadas)
    return render(request, 'mostrar_materias.html', {
        'usuario': usuario,
        'materias': materias,
        'semestre_seleccionado': semestre_seleccionado,
        'carrera_seleccionada': carrera_seleccionada,
        'carreras': carreras,
        'materias_seleccionadas':materias_seleccionadas,
    })


from django.http import HttpResponseRedirect
from django.urls import reverse


def guardar_materias(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        materias_seleccionadas = request.POST.getlist('materias')
        ubicaciones = Sala.objects.all()
        usuario = User.objects.get(id=usuario_id)

        for materia_id in materias_seleccionadas:
            materia = Materia.objects.get(id=materia_id)
            if not RelacionUsuarioMateria.objects.filter(usuario=usuario, materia=materia).exists():
                relacion = RelacionUsuarioMateria(usuario=usuario, materia=materia)
                relacion.save()
                print("Se guardó :D")
            else:
                print("La relación ya existe, no se guardó.")

        # Redirigir a la misma página donde estaba el formulario
        return redirect('mostrar_materias')


def eliminar_materias(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        materia_id = request.POST.get('materia_id')


        if materia_id:
            try:
                relacion_materia_usuario = RelacionUsuarioMateria.objects.get(materia=materia_id,usuario=usuario_id)
                relacion_materia_usuario.delete()
                print("Materia Eliminada :D")
                return redirect('mostrar_materias')
            except RelacionUsuarioMateria.DoesNotExist:
                return redirect('mostrar_materias')


