from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    # These are the three role choices
    VIEWER = 'viewer'
    ANALYST = 'analyst'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (VIEWER, 'Viewer'),
        (ANALYST, 'Analyst'),
        (ADMIN, 'Admin'),
    ]

    # This is the new field we are adding
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=VIEWER
    )

    def __str__(self):
        return f"{self.username} ({self.role})"