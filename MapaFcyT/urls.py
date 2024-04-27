from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from sim import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sim.urls')),
    path('accounts/', include('allauth.urls')),
    path('inicio/', views.inicio, name='inicio'),
]
