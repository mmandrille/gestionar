from django.contrib import admin
#Importamos nuestros modelos
from .models import Tipo_Comunicacion, Medio, Acciones, Comunicacion

#Agregamos utilidades
class MedioAdmin(admin.ModelAdmin):
     def has_module_permission(self, request):#Tiene permiso para mostrarlo?
        return False #Aqui podriamos poner una logica de validacion compleja o simplemente> return request.user.is_superuser

class Tipo_ComunicacionAdmin(admin.ModelAdmin):
     def has_module_permission(self, request):
        return False 

class ComunicacionInline(admin.TabularInline):
    model = Comunicacion

class AccionAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['id_ws', 'nombre', 'descripcion', 'organismo_ws', 'estado_id', 'monto', 'financiacion_id', 'latitud', 'longitud', 'departamento_id', 'municipio_id', 'localidad_id', 'borrado', 'publicado', 'fecha_creacion']
    inlines = [
        ComunicacionInline,
    ]







# Register your models here.
admin.site.register(Tipo_Comunicacion, Tipo_ComunicacionAdmin)#registrado para poder editar en inline/ pero no visible por el FooAdmin
admin.site.register(Medio, MedioAdmin)#registrado para poder editar en inline/ pero no visible por el FooAdmin

admin.site.register(Acciones, AccionAdmin)
#admin.site.register(Comunicacion)