from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime 

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'ADMIN (Full Dashboard Access)'),
        ('omcc', 'OMCC'),
        ('hopss', 'HOPSS'),
        ('finance', 'FINANCE'),
        ('allied', 'ALLIED HEALTH'),
        ('medical', 'MEDICAL SERVICE'),
        ('nursing', 'NURSING SERVICE'),
        ('staff', 'MEDIA STAFF'), 
    ]

    is_approved = models.BooleanField(default=False)

    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES) 

    def __str__(self):
        return self.full_name or self.username


class Request(models.Model):
    STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Approved', 'Approved'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tasks'
    )

    date_requested = models.DateTimeField(auto_now_add=True)
    date_started = models.DateField(blank=True, null=True)
    date_completed = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True) 
    
    division = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=100, blank=True)
    month = models.CharField(max_length=20, blank=True)
    project_title = models.CharField(max_length=255)
    category = models.CharField(max_length=100) 
    request_type = models.CharField(max_length=100)
    description = models.TextField()
    target_date = models.DateField()

    DELIVERY_CHOICES = [
    ('email', 'Email'),
    ('shared_drive', 'Shared Drive'),
    ]

    delivery_type = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES,
        blank=True,
        null=True
    )

    delivery_detail = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Email address or shared drive link"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Requested'
    )


    def save(self, *args, **kwargs):
        if self.user and not self.division:
            self.division = self.user.get_role_display().upper()

        if self.target_date:
            self.month = self.target_date.strftime('%B')

        if self.status == 'Approved':
            if not self.date_started:
                self.date_started = datetime.date.today()
            if not self.due_date:
                self.due_date = datetime.date.today() + datetime.timedelta(days=7)

        if self.status == 'Completed':
            if not self.date_completed:
                self.date_completed = datetime.date.today()
            self.due_date = None 

        super().save(*args, **kwargs)

    def __str__(self):
        return self.project_title
    
class RequestAttachment(models.Model):
        request = models.ForeignKey(
            Request,
            on_delete=models.CASCADE,
            related_name='attachments'
        )
        file = models.FileField(upload_to='request_attachments/')
        uploaded_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"Attachment for {self.request.project_title}"