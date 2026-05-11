from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib import admin
from django.shortcuts import redirect
from app import views  


urlpatterns = [
    path('', views.register_view, name='register'),

    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
