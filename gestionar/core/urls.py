from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    #Web Services
    url(r'^$', views.home, name='home'),

    path('org/<int:org_id>', views.list_organismos, name='list_organismos'),
    path('accion/<int:accion_id>', views.ver_accion, name='ver_accion'),
]