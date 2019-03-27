from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'getws'
urlpatterns = [
    path('<int:type_id>/', views.getws, name='getws'),
]