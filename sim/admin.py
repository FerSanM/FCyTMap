from django.contrib import admin
from .models import RelacionMateriaSala, RelacionUsuarioMateria, Sala, Actividades , Materia

#Register your models here.
admin.site.register(RelacionMateriaSala)
admin.site.register(RelacionUsuarioMateria)
admin.site.register(Sala)
admin.site.register(Actividades)
admin.site.register(Materia)