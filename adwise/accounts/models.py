from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    # Role constants
    ADMIN = "ADMIN"
    SALESPERSON = "SALESPERSON"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (SALESPERSON, "Salesperson"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,
                            default=SALESPERSON)

    def __str__(self):
        return f"{self.username} ({self.role})"