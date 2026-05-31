from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib import admin
from app import views  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pending-approval/', views.pending_approval_view, name='pending_approval'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),

    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('request/create/', views.create_request, name='create_request'),
    path('request/update/<int:pk>/', views.update_request, name='update_request'),
    path('request/delete/<int:pk>/', views.delete_request, name='delete_request'),

    path('task/update-status/<int:pk>/', views.update_task_status, name='update_task_status'),

    path('user/approve/<int:pk>/', views.approve_user, name='approve_user'),
    path('user/reject/<int:pk>/', views.reject_user, name='reject_user'),

    path('export/excel/', views.export_excel, name='export_excel'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
