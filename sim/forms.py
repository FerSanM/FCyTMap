# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Actividades
from django.core.exceptions import ValidationError
from django.utils import timezone

class ActividadesForm(forms.ModelForm):
    usuarios = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_staff=False),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Actividades
        fields = ['descripcion', 'idSala', 'fecha_actividad']  # No incluimos fecha_notificacion

    def __init__(self, *args, **kwargs):
        # Obtén los usuarios que no son staff y configúralos como seleccionados por defecto
        initial_usuarios = User.objects.filter(is_staff=False)
        kwargs.update({'initial': {'usuarios': initial_usuarios}})
        super().__init__(*args, **kwargs)

    def clean_fecha_actividad(self):
        fecha_actividad = self.cleaned_data.get('fecha_actividad')
        if fecha_actividad and fecha_actividad < timezone.now():
            raise ValidationError("La fecha de la actividad no puede ser anterior a la fecha actual.")
        return fecha_actividad