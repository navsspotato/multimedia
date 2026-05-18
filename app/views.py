from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from app.models import Request
from datetime import date

User = get_user_model()

@login_required
def dashboard_view(request):
    user = request.user
    current_role = str(user.role).lower()

    if current_role == 'admin':
        tasks = Request.objects.all().order_by('-date_requested')
        
        total_count = tasks.count()
        completed_count = tasks.filter(status='Completed').count()
        ongoing_count = tasks.filter(status='Ongoing').count()
        requested_count = tasks.filter(status='Requested').count()

        recent_tasks = tasks[:5]

        categories = [
            'Graphic Design', 'Video Editing', 'PowerPoint',
            'Photography', 'Publication', 'Web Design',
        ]
        category_stats = []
        for cat in categories:
            cat_tasks = tasks.filter(category__iexact=cat)
            category_stats.append({
                'name': cat,
                'count': cat_tasks.count(),
                'completed': cat_tasks.filter(status='Completed').count(),
                'ongoing': cat_tasks.filter(status='Ongoing').count(),
                'requested': cat_tasks.filter(status='Requested').count(),
            })

        context = {
            'tasks': tasks,
            'recent_tasks': recent_tasks,
            'category_stats': category_stats,
            'total_count': total_count,
            'completed_count': completed_count,
            'ongoing_count': ongoing_count,
            'requested_count': requested_count,
            'status_choices': ['Requested', 'Approved', 'Ongoing', 'Completed'],
            'staff_list': User.objects.filter(role='staff'), 
        }
        return render(request, 'admin_dashboard.html', context)

    else:
        DIVISION_UNITS = {
            'hopss': [
                'Engineering & Facilities Management Section',
                'Biomed Unit', 'Building Facilities Unit',
                'Powerhouse Unit', 'Transportation Unit',
                'Human Resource Management Section',
                'Materials Management Section',
                'Procurement Section', 'General Services',
                'Housekeeping', 'Linen and Laundry',
            ],
            'allied': [
                'Health Information Management Section',
                'Admitting & Information Unit', 'OPD Records',
                'Nutrition & Dietetics Services',
                'Pharmacy Section', 'Social Service',
            ],
            'medical': [
                'Emergency Department', 'HEMS / DRRM-H',
                'Out Patient Services', 'Pathology & Laboratories',
                'Blood Bank', 'Molecular Laboratory', 'Paywards',
                'Radiology', 'Nuclear Medicine', 'Cancer Center',
                'Mental Health', 'Brain and Spine Center',
                'Cardiovascular Care', 'Eye Care',
                'Infectious Disease & Tropical Medicine',
                'Lung Care', 'Neonatal Care', 'Orthopedic Care',
                'Physical Rehabilitation Medicine',
                'Renal Care & Transplant Center', 'Trauma Care',
                'Anesthesiology', 'Family & Community Medicine',
                'Internal Medicine', 'Pediatrics',
                'Obstetrics & Gynecology',
                'Otorhinolaryngology - Head & Neck Surgery',
                'Surgery', 'Dental Medicine',
            ],
            'nursing': [
                'Amethyst Ward', 'Behavioral Medicine',
                'Medical Ward', 'OB-Gyne Ward', 'Pay Wards',
                'Pearl Ward', 'Pediatrics Ward', 'Surgery Ward',
                'Florence Nightingale', 'Diamond Ward', 'Garnet Ward',
                'Delivery Room', 'Intensive Care Unit', 'NICU',
                'PACU', 'PICU', 'SICU',
                'Frontline/Referring Services',
                'Specialty Centers', 'Clinics', 'HACT', 'TB DOTS',
            ],
            'finance': [
                'Accounting Section', 'Billing & Claims Section',
                'Budget Section', 'Cash Management Section',
            ],
            'omcc': ['OMCC'],
        }

        user_units = DIVISION_UNITS.get(current_role, [])
        requests = Request.objects.filter(user=user).order_by('-date_requested')
        return render(request, 'user_dashboard.html', {
            'requests': requests,
            'all_requests_count': requests.count(),
            'pending_requests_count': requests.filter(status='Requested').count(),
            'user_units': user_units,
        })

@login_required
def update_task_status(request, pk):
   
    task = get_object_or_404(Request, pk=pk)

    if request.method == "POST" and str(request.user.role).lower() == 'admin':
        status = request.POST.get("status")
        staff_id = request.POST.get("assigned_to")

        if status:
            task.status = status
        if staff_id:
            try:
                task.assigned_to = User.objects.get(id=staff_id)
            except User.DoesNotExist:
                pass

        task.save() 
    return redirect('dashboard')

@login_required
def create_request(request):
    if request.method == 'POST':
        # Your foundation logic is perfect here
        target_date_raw = request.POST.get('target_date')
        target_date = date.fromisoformat(target_date_raw) if target_date_raw else None

        Request.objects.create(
            user=request.user,
            unit=request.POST.get('division'),
            project_title=request.POST.get('project_title'),
            category=request.POST.get('category'),
            request_type=request.POST.get('request_type'),
            description=request.POST.get('description'),
            target_date=target_date,
        )
        return redirect('dashboard')
    return render(request, 'create_request.html')

@login_required
def update_request(request, pk):
    task = get_object_or_404(Request, pk=pk)
    
    if request.method == 'POST':
        task.project_title = request.POST.get('project_title', task.project_title)
        task.category = request.POST.get('category', task.category)
        task.request_type = request.POST.get('request_type', task.request_type)
        task.status = request.POST.get('status', task.status)
        task.division = request.POST.get('division', task.division)

        due_date_raw = request.POST.get('due_date')
        if due_date_raw:
            task.due_date = date.fromisoformat(due_date_raw)
        
        date_started_raw = request.POST.get('date_started')
        if date_started_raw:
            task.date_started = date.fromisoformat(date_started_raw)
            
        date_completed_raw = request.POST.get('date_completed')
        if date_completed_raw:
            task.date_completed = date.fromisoformat(date_completed_raw)

        staff_id = request.POST.get('assigned_to')
        if staff_id:
            try:
                task.assigned_to = User.objects.get(id=staff_id)
            except User.DoesNotExist:
                pass

        task.save()
        return redirect('dashboard')

    context = {
        'task': task,
        'staff_list': User.objects.filter(role='staff'),
        'status_choices': ['Requested', 'Approved', 'Ongoing', 'Completed'],
    }
    return render(request, 'update_request.html', context)

@login_required
def delete_request(request, pk):
    req = get_object_or_404(Request, pk=pk)
    if request.user.role == 'admin' or req.user == request.user:
        req.delete()
    return redirect('dashboard')


@login_required
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

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            full_name=full_name,
            role=role.lower()
        )
        return redirect('login')
    return render(request, 'register.html')

