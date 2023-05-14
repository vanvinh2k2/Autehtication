from django.urls import path
from . import views

urlpatterns = [
    path('', views.Init , name='init'),
    path('login/', views.Login , name='login'),
    path('home/', views.Home , name='home'),
    path('logout/', views.Logout , name='logout'),
    path('change-password/<token>/', views.ChangePassword , name='change-password'),
    path('forget-password/', views.ForgetPassword , name='forget-password'),
]