from django.shortcuts import render
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required

#Import Particulares
from .models import Organismo, Acciones, Comunicacion, IMPORTANCIA


# Create your views here.
def home(request):
    organismos = Organismo.objects.annotate(count=Count('acciones')).order_by('-count')
    return render(request, 'home.html', {"organismos": organismos})

def home_prioridad(request):
    #organismos = Organismo.objects.annotate(count=Count('acciones')).order_by('-count')
    acciones = Acciones.objects.annotate(count=Count('comunicaciones')).order_by('importancia', '-count', 'organismo_ws')[:100]
    return render(request, 'home_prioridad.html', {"acciones": acciones, "importancia": IMPORTANCIA})

def list_organismos(request, org_id):
    organismo = Organismo.objects.get(pk=org_id)
    return render(request, 'organismo.html', {"organismo": organismo, "importancia": IMPORTANCIA})

def ver_accion(request, accion_id):
    accion = Acciones.objects.get(pk=accion_id)
    return render(request, 'accion.html', {"accion": accion})

def ver_comunicacion(request, comunicado_id):
    comunicacion = Comunicacion.objects.get(pk=comunicado_id)
    return render(request, 'comunicado.html', {"comunicacion": comunicacion})
