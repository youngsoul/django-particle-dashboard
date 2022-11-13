from django.db import models
from django.contrib.auth.models import AbstractUser
from particle_devices.models import ParticleDevice

# Create your models here.
class CustomUser(AbstractUser):
    # add note about the user
    notes = models.TextField(null=True, blank=True)

    particle_devices = models.ManyToManyField(ParticleDevice, through='UsersParticleDevice', blank=True)

class UsersParticleDevice(models.Model):
    person = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    device = models.ForeignKey(ParticleDevice, on_delete=models.CASCADE)
    can_see_functions = models.BooleanField(default=False)
    can_call_functions = models.BooleanField(default=False)
    can_view_events = models.BooleanField(default=False)
    can_send_events = models.BooleanField(default=False)
