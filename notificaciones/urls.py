from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('mis-notificaciones/', views.mis_notificaciones, name='mis_notificaciones'),
    
]
