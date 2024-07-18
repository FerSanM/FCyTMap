from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from allauth.socialaccount import providers
from allauth.socialaccount.urls import urlpatterns as socialaccount_urls
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from allauth.socialaccount import providers
from allauth.socialaccount.urls import urlpatterns as socialaccount_urls

from sim import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sim.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login', ),
    path('inicio/', views.inicio, name='inicio'),
    path('iniciosin/', views.iniciosin, name='iniciosin'),
]
#urlpatterns += socialaccount_urls