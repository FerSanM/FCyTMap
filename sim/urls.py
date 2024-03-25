from django.urls import path
from . import views

urlpatterns = [
    path('sign_in', views.sign_in, name='sign_in'),
    path('inicio', views.inicio, name='inicio'),
    path('sign-out', views.sign_out, name='sign_out'),
    # path('materias/', views.mostrar_materias, name='mostrar_materias'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('guardar_materias/', views.guardar_materias, name='guardar_materias'),
    path('carreras/', views.get_carreras, name='get_carreras'),
    path('materias/<int:idcarrera>/<int:semestre>', views.get_materias, name='get_materias'),
    path('tabla/', views.get_tabla, name='get_tabla'),
    path('eliminar_relacion/<int:relacion_id>/', views.eliminar_relacion, name='eliminar_relacion')
]
