from django.contrib import admin
#Importamos nuestros modelos
from .models import Tipo_Comunicacion, Medio, Acciones, Comunicacion

#Agregamos utilidades
class AccionAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'descripcion']

# Register your models here.
admin.site.register(Tipo_Comunicacion)
admin.site.register(Medio)

admin.site.register(Acciones, AccionAdmin)
admin.site.register(Comunicacion)