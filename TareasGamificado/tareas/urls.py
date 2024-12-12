from django.urls import path
from tareas import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('accounts/ login/', views.LoginVista, name='login'),
]
