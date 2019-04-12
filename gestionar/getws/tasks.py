#Traemos el sistema de Backgrounds
import requests
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from background_task import background
#Import Personales
from core.models import Acciones, Estado, Financiacion, Organismo, Departamento, Municipio, Localidad

#Definimos Funciones
def dividir_procesamiento_paginas(max_por_bloque):
    nombre_tarea = "Cargar_Info-" + str(datetime.datetime.now())[0:10] + '-' + str(datetime.datetime.now())[11:16]
    #Nos loggeamos en el server
    url_login = "http://obras.jujuy.gob.ar/obras/web/index.php/wsusuarios/login?username=ws_client&password=1qazZAQ!"
    respuesta_login = requests.get(url_login)
    #Obtenemos el token
    token = respuesta_login.json()['token']
    #Comenzamos a retirar las paginas de Obras
    url_obras = "http://obras.jujuy.gob.ar/obras/web/index.php/wsobras/obras?desde=1900-01-01&hasta=9999-12-31&sortField=nombre&sortDirection=DESC&page=1"
    respuesta_obras = requests.get(url_obras, auth=(token, token))
    data_obras = respuesta_obras.json()
    cant = data_obras['nroPaginas']
    x = 0
    while x+max_por_bloque < cant:
            obtener_paginas(token, x, x+max_por_bloque, schedule=int(x/10), queue=nombre_tarea)
            x+= max_por_bloque
    obtener_paginas(token, x, cant, schedule=int(x/10), queue=nombre_tarea)
    return nombre_tarea


@background(schedule=60)
def obtener_paginas(token, pagina_begda, pagina_endda):
    for x in range(pagina_begda, pagina_endda + 1):
        url_obras = "http://obras.jujuy.gob.ar/obras/web/index.php/wsobras/obras?desde=1900-01-01&hasta=9999-12-31&sortField=nombre&sortDirection=DESC&page=" + str(x)
        respuesta_obras = requests.get(url_obras, auth=(token, token))
        data_obras = respuesta_obras.json()
        cant = data_obras['nroPaginas']
        for ws_obra in data_obras['datos']:
                accion = Acciones.objects.filter(id_ws=ws_obra['ID']).first()
                if accion is None:
                        accion = Acciones()
                #Aqui hacemos todos los transpasos directos
                accion.id_ws = ws_obra['ID']
                accion.nombre = ws_obra['NOMBRE']
                accion.descripcion = ws_obra['DESCRIPCION']
                accion.fecha_creacion = ws_obra['FECHA_CREACION'][0:10]
                #Conversiones Simpls
                if ws_obra['MONTO'] is not None: accion.monto = ws_obra['MONTO']
                if ws_obra['LATITUD'] is not None: accion.latitud = ws_obra['LATITUD']
                if ws_obra['LONGITUD'] is not None: accion.longitud = ws_obra['LONGITUD']
                if ws_obra['BORRADO'] == 1: accion.borrado = True
                if ws_obra['PUBLICADO'] == 1: accion.publicado = True
                #Creacion con campos de subtablas
                #Estado
                try: accion.estado_id = Estado.objects.get(nombre=ws_obra['ESTADO'])
                except ObjectDoesNotExist:
                        estado = Estado(nombre=ws_obra['ESTADO'])
                        estado.save()
                        accion.estado_id = estado
                #Organismo
                try: accion.organismo_ws = Organismo.objects.get(nombre=ws_obra['MINISTERIO'])
                except ObjectDoesNotExist:
                        organismo = Organismo(nombre=ws_obra['MINISTERIO'])
                        organismo.save()
                        accion.organismo_ws = organismo
                #Financiacion
                try: accion.financiacion_id = Financiacion.objects.get(nombre=ws_obra['TIPO_FINANCIACION'])
                except ObjectDoesNotExist:
                        financiacion = Financiacion(nombre=ws_obra['TIPO_FINANCIACION'])
                        financiacion.save()
                        accion.financiacion_id = financiacion
                #Departamento
                try: accion.departamento_id = Departamento.objects.get(nombre=ws_obra['DEPARTAMENTO'])
                except ObjectDoesNotExist:
                        departamento = Departamento(nombre=ws_obra['DEPARTAMENTO'])
                        departamento.save()
                        accion.departamento_id = departamento
                #Municipio
                try: accion.municipio_id = Municipio.objects.get(nombre=ws_obra['MUNICIPIO'])
                except ObjectDoesNotExist:
                        municipio = Municipio(nombre=ws_obra['MUNICIPIO'])
                        municipio.save()
                        accion.municipio_id = municipio
                #Localidad
                try: accion.localidad_id = Localidad.objects.get(nombre=ws_obra['LOCALIDAD'])
                except ObjectDoesNotExist:
                        localidad = Localidad(nombre=ws_obra['LOCALIDAD'])
                        localidad.save()
                        accion.localidad_id = localidad
                accion.save()