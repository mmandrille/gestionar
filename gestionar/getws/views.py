import requests
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def getws(request, type_id):
    print('Haciendo login...')
    url_login = "http://obras.jujuy.gob.ar/obras/web/index.php/wsusuarios/login?username=ws_client&password=1qazZAQ!"
    respuesta_login = requests.get(url_login)
    token = respuesta_login.json()['token']

    print('Pidiendo una pagina de data de TODAS las obras...')
    url_obras = "http://obras.jujuy.gob.ar/obras/web/index.php/wsobras/obras?desde=1900-01-01&hasta=9999-12-31&sortField=nombre&sortDirection=ASC&page=1"
    respuesta_obras = requests.get(url_obras, auth=(token, token))
    data_obras = respuesta_obras.json()

    print('Cantidad de paginas:', data_obras['nroPaginas'])
    print('Nombre de la primera obra:', data_obras['datos'][0]['NOMBRE'])
    return HttpResponse("En la consola deberias ver los resultados")