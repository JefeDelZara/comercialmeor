from django.urls import path
from . import views



app_name = 'login'

urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Ruta para cerrar sesión
    
]

