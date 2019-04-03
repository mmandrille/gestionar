#Standard imports
from __future__ import unicode_literals
import datetime
#Django imports
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#Extra modules import
from tinymce.models import HTMLField

# Create your models here.
class Estado(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    def __str__(self):
            return self.nombre

class Organismo(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    def __str__(self):
            return self.nombre

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

IMPORTANCIA = (
    (1, 'Prioritaria'),
    (3, 'Intermedia'),
    (6, 'Leve'),
    (9, 'Sin Marcar'),
)

class Acciones(models.Model):
    id_ws = models.IntegerField(unique=True)
    nombre = models.CharField('Nombre', max_length=100)
    importancia = models.IntegerField(choices=IMPORTANCIA, default=9)
    estado_id = models.ForeignKey(Estado, on_delete=models.CASCADE)#Estado
    organismo_id = models.ForeignKey(Organismo, on_delete=models.CASCADE)#Organismo
    descripcion = HTMLField()
    monto = models.IntegerField(default=0, blank=True, null=True)
    financiacion_id = models.ForeignKey(Financiacion, on_delete=models.CASCADE)#Financiacion
    latitud = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    longitud = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    departamento_id = models.ForeignKey(Departamento, on_delete=models.CASCADE)#Departamento
    municipio_id = models.ForeignKey(Municipio, on_delete=models.CASCADE)#Municipio
    localidad_id = models.ForeignKey(Localidad, on_delete=models.CASCADE)#localidad
    borrado = models.BooleanField(default=False)
    publicado = models.BooleanField('Publicable', default=False)
    fecha_creacion = models.DateField(default=datetime.date.today)
    def __str__(self):
            return self.nombre

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
    descripcion = HTMLField()
    monto = models.IntegerField(default=0, blank=True, null=True)
    fecha_creacion = models.DateField(default=datetime.date.today)