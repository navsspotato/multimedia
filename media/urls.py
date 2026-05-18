from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib import admin
from app import views  

urlpatterns = [
    path('', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('request/create/', views.create_request, name='create_request'),
    path('request/update/<int:pk>/', views.update_request, name='update_request'),
    path('request/delete/<int:pk>/', views.delete_request, name='delete_request'),

    path('task/update-status/<int:pk>/', views.update_task_status, name='update_task_status'),

    path('admin/', admin.site.urls),
]
