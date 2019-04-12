from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    #Web Services
    url(r'^$', views.home, name='home'),
    path('prio/', views.home_prioridad, name='home_prioridad'),
    url('^contacto/$', views.contacto, name='contacto'),

    path('org/<int:org_id>', views.list_organismos, name='list_organismos'),
    path('localidad/<int:localidad_id>', views.list_localidad, name='list_localidad'),
    path('accion/<int:accion_id>', views.ver_accion, name='ver_accion'),
    path('comunicado/<int:comunicado_id>', views.ver_comunicacion, name='ver_comunicacion'),

    #Testing mail
    path('send/mail_semanal', views.test_mail_semanal, name='test_mail_semanal'),

    #task_manager
    path('task_progress/<str:queue_name>', views.task_progress, name='task_progress'),
]