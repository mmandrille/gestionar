import requests
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
#Nuestros imports
from core.models import Acciones, Estado, Financiacion, Organismo, Departamento, Municipio, Localidad
from .tasks import dividir_procesamiento_paginas
from core.views import task_progress

# Create your views here.
def getws(request, block_pages):
    tarea = dividir_procesamiento_paginas(block_pages)
    return HttpResponseRedirect("/task_progress/"+tarea)