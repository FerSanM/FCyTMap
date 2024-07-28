from django.urls import path
from . import views

urlpatterns = [

    # path('sign-out', views.sign_out, name='sign_out'),
    # path('materias/', views.mostrar_materias, name='mostrar_materias'),
    # path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('inicio/guardar_materias/', views.guardar_materias, name='guardar_materias'),
    path('inicio/carreras/', views.get_carreras, name='get_carreras'),
    path('inicio/materias/<int:idcarrera>/<int:semestre>', views.get_materias, name='get_materias'),
    path('inicio/notificaciones/', views.get_notificaciones, name='get_notificaciones'),
    path('inicio/tabla/', views.get_tabla, name='get_tabla'),
    path('inicio/eliminar_relacion/<int:relacion_id>/', views.eliminar_relacion, name='eliminar_relacion'),
    path('inicio/eliminar_evento/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('inicio/tabla_eventos/', views.get_tablaeventos, name='get_tablaeventos'),
    path('inicio/listarsalas/', views.get_sala, name='get_sala'),
    path('inicio/obtener_evento/<int:evento_id>/', views.obtener_evento, name='obtener_evento'),
    path('inicio/editar_evento/', views.editar_evento, name='editar_evento'),
    path('inicio/marcar_visto/', views.marcar_visto, name='marcar_visto'),
    path('inicio/guardar_evento/', views.guardar_evento, name='guardar_evento'),
    path('inicio/valorar/', views.valorar, name='valorar'),
    path('custom_logout/', views.custom_logout, name='custom_logout'),
    path('eliminar_cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('404-notfound/', views.not_found, name='not_found'),

]
