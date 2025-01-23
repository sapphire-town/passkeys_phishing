from django.db import models

# Create your models here.

# accounts/models.py-chat gpt
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    webauthn_credentials = models.JSONField(default=list)  # To store passkey data
    # Add custom fields if needed
    additional_field = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
