from django.db import models
from .utils import get_particle_cloud


# Create your models here.
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ParticleDevice(TimeStampMixin):
    # emperically these ids appear to be 24 characters, but why tempt fate
    device_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    online = models.BooleanField(default=False)
    device_type = models.CharField(max_length=128, blank=True, null=True)

    device_details = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.device_id}|{self.name}"

    def particle_refresh(self):
        # refresh the state of the particledevice
        cloud = get_particle_cloud()
        device_info = cloud.get_device_info(self.device_id)
        self.device_details = device_info
        self.name = device_info['name']
        self.online = device_info['online']
        # Indicates the type of device. Example values are 6 for Photon, 10 for Electron, 12 for Argon, 13 for Boron.
        match device_info['platform_id']:
            case 6:
                self.device_type = "Photon"
            case 10:
                self.device_type = "Electron"
            case 12:
                self.device_type = "Argon"
            case 13:
                self.device_type = "Boron"
            case _:
                self.device_type = "Unknown"

        self.save()
