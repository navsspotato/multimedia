from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Request


# CUSTOM USER ADMIN
@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    list_display = (
        'username',
        'full_name',
        'email',
        'role',
        'is_staff',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'Custom Fields',
            {
                'fields': (
                    'full_name',
                    'role',
                )
            },
        ),
    )


# REQUEST ADMIN
@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):

    list_display = (
        'date_requested',
        'division',
        'project_title',
        'category',
        'request_type',
        'target_date',
        'status',
        'assigned_to',
    )

    list_filter = (
        'status',
        'division',
        'category',
    )

    search_fields = (
        'project_title',
        'division',
    )