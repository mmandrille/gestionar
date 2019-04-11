#Import Standard
from django.forms import ModelForm

from .models import Acciones, IMPORTANCIA
#creamos ModelForm
class AccionesForm(ModelForm):
    class Meta:
        model = Acciones
        fields = ['importancia', 'localidad_id', 'nombre',]
        labels = {
        "importancia": "Importancia",
        "localidad_id": "Localidad",
        "nombre": "Nombre",}
    def __init__(self, *args, **kwargs):
        super(AccionesForm, self).__init__(*args, **kwargs)
        self.fields['importancia'].required = False
        self.fields['importancia'].initial = 0
        self.fields['localidad_id'].required = False
        self.fields['nombre'].required = False
        