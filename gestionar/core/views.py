from django.shortcuts import render
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required

#Import Particulares
from .models import Organismo, Acciones


# Create your views here.
def home(request):
    #organismos = Organismo.objects.all()
    organismos = Organismo.objects.annotate(count=Count('acciones')).order_by('count')
    return render(request, 'home.html', {"organismos": organismos})

def list_organismos(request, org_id):
    organismo = Organismo.objects.get(pk=org_id)
    return render(request, 'organismo.html', {"organismo": organismo})

def ver_accion(request, accion_id):
    accion = Acciones.objects.get(pk=accion_id)
    return render(request, 'accion.html', {"accion": accion})
