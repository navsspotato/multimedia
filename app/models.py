from django.contrib.auth.models import AbstractUser
from django.db import models


# CUSTOM USER MODEL
class User(AbstractUser):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('omcc', 'OMCC'),
        ('hopss', 'HOPSS'),
        ('finance', 'Finance'),
        ('allied', 'Allied Health'),
        ('medical', 'Medical'),
        ('nursing', 'Nursing'),
    ]

    full_name = models.CharField(max_length=255)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return self.full_name


# REQUEST MODEL
class Request(models.Model):

    STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Approved', 'Approved'),
        ('Scheduled', 'Scheduled'),
        ('Ongoing', 'Ongoing'),
        ('Done', 'Done'),
    ]

    CATEGORY_CHOICES = [
        ('Graphic Design', 'Graphic Design'),
        ('Video Editing', 'Video Editing'),
        ('PowerPoint', 'PowerPoint'),
        ('Photography', 'Photography'),
        ('Publication', 'Publication'),
        ('Web Design', 'Web Design'),
    ]

    TYPE_CHOICES = [
        ('PPT Presentation', 'PPT Presentation'),
        ('Tarp Design', 'Tarp Design'),
        ('Video Editing', 'Video Editing'),
        ('Certificate', 'Certificate'),
        ('Social Media Pubmat', 'Social Media Pubmat'),
        ('Newsletter', 'Newsletter'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date_requested = models.DateTimeField(
        auto_now_add=True
    )

    division = models.CharField(max_length=100)

    project_title = models.CharField(max_length=255)

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    request_type = models.CharField(
        max_length=100,
        choices=TYPE_CHOICES
    )

    description = models.TextField()

    target_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Requested'
    )

    assigned_to = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.project_title