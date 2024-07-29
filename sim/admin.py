# admin.py
from django.contrib import admin
from .models import Actividades
from .forms import ActividadesForm
from django.contrib.auth.models import User
from datetime import timedelta
from .models import RelacionMateriaSala, RelacionUsuarioMateria, Sala, Actividades , Materia
class ActividadesAdmin(admin.ModelAdmin):
    form = ActividadesForm

    def save_model(self, request, obj, form, change):
        if not change:  # Si se está creando una nueva instancia
            usuarios = User.objects.filter(is_staff=False)  # Obtener todos los usuarios no staff
            fecha_actividad = form.cleaned_data['fecha_actividad']
            fecha_notificacion = fecha_actividad - timedelta(weeks=1)  # Calcular fecha_notificacion como una semana antes

            for usuario in usuarios:
                Actividades.objects.create(
                    descripcion=obj.descripcion,
                    idSala=obj.idSala,
                    idUsuario=usuario,
                    fecha_actividad=fecha_actividad,
                    fecha_notificacion=fecha_notificacion,
                    vistousuario=obj.vistousuario
                )
        else:
            # Para la edición de una actividad existente, usa el valor de fecha_actividad proporcionado
            obj.fecha_notificacion = obj.fecha_actividad - timedelta(weeks=1)
            super().save_model(request, obj, form, change)

admin.site.register(Actividades, ActividadesAdmin)

admin.site.register(RelacionMateriaSala)
admin.site.register(RelacionUsuarioMateria)
admin.site.register(Sala)
admin.site.register(Materia)