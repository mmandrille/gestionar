#Decoradores
from django.contrib.admin.views.decorators import staff_member_required

#Import normales
from django.shortcuts import render
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
#Task Manager Models
from background_task.models import Task as bg_Tasks
from background_task.models_completed import CompletedTask as bg_CompletedTask
#Import de otros modulos
from background_task import background
from .models import Organismo, Acciones, Comunicacion, IMPORTANCIA, obtener_organismos
from .ModelForm import AccionesForm
from .tasks import mail_semanal


# Create your views here.
def buscador(request):
    if request.method == 'POST':
        form = AccionesForm(request.POST)
        if form.is_valid():
            acciones = Acciones.objects.all()
            if form.cleaned_data.get('importancia'):
                print(form.cleaned_data.get('importancia'))
                acciones = acciones.filter(importancia=form.cleaned_data.get('importancia'))
            if form.cleaned_data.get('localidad_id'):
                acciones = acciones.filter(localidad_id=form.cleaned_data.get('localidad_id'))
            if form.cleaned_data.get('nombre'):
                acciones = acciones.filter(nombre__icontains=form.cleaned_data.get('nombre'))
            return acciones.annotate(count=Count('comunicaciones')).order_by('-importancia', '-count', 'organismo_ws')[:50]

def home(request):
    acciones = buscador(request)
    if acciones: return render(request, 'buscador.html', {"acciones": acciones, "importancia": IMPORTANCIA})
    else:
        form = AccionesForm()
        organismos = Organismo.objects.annotate(count=Count('acciones')).order_by('-count')
        return render(request, 'home.html', {"organismos": organismos, 'form':form})

def home_prioridad(request):
    acciones = buscador(request)
    if acciones: return render(request, 'buscador.html', {"acciones": acciones, "importancia": IMPORTANCIA})
    else:
        buscador(request)
        form = AccionesForm()
        acciones = Acciones.objects.annotate(count=Count('comunicaciones')).order_by('-importancia', '-count', 'organismo_ws')[:100]
        return render(request, 'home_prioridad.html', {"acciones": acciones, 'form':form, "importancia": IMPORTANCIA})

def contacto(request):
    return render(request, 'contacto.html', { })

def list_organismos(request, org_id):
    organismo = Organismo.objects.get(pk=org_id)
    return render(request, 'organismo.html', {"organismo": organismo, "importancia": IMPORTANCIA})

def ver_accion(request, accion_id):
    orgs_ws = obtener_organismos()
    accion = Acciones.objects.get(pk=accion_id)
    return render(request, 'accion.html', {"accion": accion, "orgs_ws": orgs_ws})

def ver_comunicacion(request, comunicado_id):
    comunicacion = Comunicacion.objects.get(pk=comunicado_id)
    return render(request, 'comunicado.html', {"comunicacion": comunicacion})

@staff_member_required
def test_mail_semanal(request):
    mail_semanal(verbose_name="Envio de Mails Semanale", creator=request.user)
    return render(request, 'resultado.html', {'texto': 'Los mails fueron enviados con exito', })

@staff_member_required
def task_progress(request, queue_name):
    tareas_en_progreso = bg_Tasks.objects.filter(queue= queue_name)
    tareas_terminadas = bg_CompletedTask.objects.filter(queue= queue_name)
    return render(request, 'task_progress.html', {'tarea_queue': queue_name, 
                                                'tareas_totales': (len(tareas_en_progreso)+len(tareas_terminadas)) ,
                                                'tareas_en_cola': len(tareas_en_progreso), 
                                                'tareas_terminadas': len(tareas_terminadas),
                                                "bool_refresh": True })