#Standard imports
from __future__ import unicode_literals
import datetime
#Django imports
from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import json
#Extra modules import
from tinymce.models import HTMLField

#Funciones extra y Choice Field
def obtener_organismos():#Funcion que obtiene del sistema de organigrama los organismos disponibles
	organismos = cache.get("organismos")
	if organismos is None:
		r = requests.get('http://organigrama.jujuy.gob.ar/ws_org/')
		orgs = json.loads(r.text)['data']
		organismos = list()
		for org in orgs:
			organismos.append((org['id'],org['nombre']))
		cache.set("organismos", organismos, 10 * 60)  # guardar la data por 10 minutos, y después sola expira
	return organismos

IMPORTANCIA = (
    (0, 'Indefinida'),
    (3, 'Leve'),
    (6, 'Intermedia'),
    (9, 'Prioritaria'),
)

# Create your models here.
class Estado(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    def __str__(self):
            return self.nombre

class Organismo(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL ,blank=True, null=True)
    def __str__(self):
            return self.nombre
    def cantidad_comunicados(self):
        return Comunicacion.objects.filter(id_accion__in=Acciones.objects.filter(organismo_ws=self)).count()
    def sin_comunicar(self):
        return Acciones.objects.filter(organismo_ws=self, comunicaciones=None).count()
    def get100_acciones(self):
        return Acciones.objects.filter(organismo_ws=self)[:100]

class Financiacion(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    def __str__(self):
            return self.nombre

class Departamento(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    def __str__(self):
            return self.nombre

class Municipio(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    def __str__(self):
            return self.nombre

class Localidad(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    def __str__(self):
            return self.nombre

class Acciones(models.Model):
    organismo = models.PositiveIntegerField(choices= obtener_organismos(), default=0)
    importancia = models.IntegerField(choices=IMPORTANCIA, default=0)
    id_ws = models.IntegerField(unique=True)
    nombre = models.CharField('Nombre', max_length=100)
    estado_id = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name="acciones")#Estado
    organismo_ws = models.ForeignKey(Organismo, on_delete=models.CASCADE, related_name="acciones")#Organismo
    descripcion = HTMLField()
    monto = models.IntegerField(default=0, blank=True, null=True)
    financiacion_id = models.ForeignKey(Financiacion, on_delete=models.CASCADE, related_name="acciones")#Financiacion
    latitud = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    longitud = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    departamento_id = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="acciones")#Departamento
    municipio_id = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name="acciones")#Municipio
    localidad_id = models.ForeignKey(Localidad, on_delete=models.CASCADE, related_name="acciones")#localidad
    borrado = models.BooleanField(default=False)
    publicado = models.BooleanField('Publicable', default=False)
    fecha_creacion = models.DateField(default=datetime.date.today)
    def __str__(self):
            return self.nombre
    class Meta:
        ordering = ('-importancia', 'organismo', )

class Tipo_Comunicacion(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    def __str__(self):
            return self.nombre

class Medio(models.Model):
    tipo = models.ForeignKey(Tipo_Comunicacion, on_delete=models.CASCADE)
    nombre = models.CharField('Nombre', max_length=100)
    def __str__(self):
            return self.nombre

class Comunicacion(models.Model):
    id_accion = models.ForeignKey(Acciones, on_delete=models.CASCADE, related_name="comunicaciones")
    tipo = models.ForeignKey(Tipo_Comunicacion, on_delete=models.CASCADE)
    medio = models.ForeignKey(Medio, on_delete=models.CASCADE)
    titulo = models.CharField('Titulo', max_length=100)
    descripcion = HTMLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    monto = models.IntegerField(default=0, blank=True, null=True)
    fecha_creacion = models.DateField(default=datetime.date.today)
    def __str__(self):
        return self.id_accion.nombre + ' > ' + self.titulo