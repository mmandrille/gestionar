#Traemos el sistema de Backgrounds
from background_task import background
from django.core import mail
from django.template.loader import render_to_string
from gestionar.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
#Import Personales
from .models import Organismo
from .functions import delete_tags


#Tareas
@background(schedule=1)
def enviar_mails():
    organismo_sinuser = list()
    for org in Organismo.objects.all():
        if org.usuario:#Si el Organismo tiene definido Responsable
            acciones_prioritarias = org.acciones.filter(importancia=9, comunicaciones=None)
            acciones_intermedias = org.acciones.filter(importancia=6, comunicaciones=None)
            acciones_leves = org.acciones.filter(importancia=3, comunicaciones=None)
            acciones_sinmarcar = org.acciones.filter(importancia=0, comunicaciones=None)
            #Abiento Obtenido Acciones sin comunicar
            mail_subject = 'Reporte Semanal de Gestionar'
            message = render_to_string('reporte_semanal.html', {
                    'usuario': org.usuario,
                    'organismo': org,
                    'acciones_prioritarias': acciones_prioritarias,
                    'acciones_intermedias': acciones_intermedias,
                    'acciones_leves': acciones_leves,
                    'acciones_sinmarcar': acciones_sinmarcar,})
            email = EmailMessage(mail_subject, message, to=[org.usuario.email])
            email.send()
        else:#Si hay Organismo sin responsable
            organismo_sinuser.append(org)
    if organismo_sinuser is not []:#Si existen organismos sin usuario
        superusers = User.objects.filter(is_superuser=True)#Obtenemos todos los superusuarios del sistema
        for superuser in superusers:#Por cada uno de ellos
            mail_subject = 'Reporte Semanal Administrativo Gestionar'#Le vamos a mandar un mail avisando que hay organismos sin responsable
            message = render_to_string('reporte_semanal_admin.html', {
                    'usuario': superuser,
                    'organismos': organismo_sinuser,})
            email = EmailMessage(mail_subject, message, to=[superuser.email])
            email.send()
        
        