from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    # add note about the user
    notes = models.TextField(null=True, blank=True)
