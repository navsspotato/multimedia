from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required

User = get_user_model()


@login_required
def dashboard_view(request):

    if request.user.role == 'admin':
        return render(request, 'admin_dashboard.html')

    else:
        return render(request, 'user_dashboard.html')


def logout_view(request):

    logout(request)

    return redirect('login')


def register_view(request):

    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # PASSWORD VALIDATION
        if password != confirm_password:

            return render(
                request,
                'register.html',
                {
                    'error': 'Passwords do not match'
                }
            )

        # ADMIN LIMIT VALIDATION
        admin_count = User.objects.filter(
            role='admin'
        ).count()

        if role == 'admin' and admin_count >= 2:

            return render(
                request,
                'register.html',
                {
                    'error': 'Maximum number of admins reached'
                }
            )

        # CREATE USER
        user = User.objects.create_user(

            username=email,

            email=email,

            password=password,

            full_name=full_name,

            role=role.lower()
        )

        return redirect('login')

    return render(request, 'register.html')