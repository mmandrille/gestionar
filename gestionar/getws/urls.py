from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'getws'
urlpatterns = [
    path('<int:max_pages>/', views.getws, name='getws'),
]