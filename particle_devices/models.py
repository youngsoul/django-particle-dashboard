from django.db import models
from .utils import get_particle_cloud
from .event_subscription import float_event_handler, integer_event_handler, string_event_handler
import logging

app_logger = logging.getLogger('myapp')

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

    def get_variable_names(self):
        if 'variables' in self.device_details:
            return list(self.device_details['variables'].keys())
        else:
            return []

    def update_event_subscription(self, particle_event):
        # always unsubscribe to refresh the event subscription
        get_particle_cloud().devices[self.name].unsubscribe(particle_event.name)
        if particle_event.subscribe:
            app_logger.info(f"Event Subscribe: {particle_event}")
            # if any of the events are currently subscribed, make sure to unsubscribe first
            if particle_event.event_type == ParticleDeviceEvent.EventType.FLOAT:
                get_particle_cloud().devices[self.name].subscribe(particle_event.name, float_event_handler)
            elif particle_event.event_type == ParticleDeviceEvent.EventType.INTEGER:
                get_particle_cloud().devices[self.name].subscribe(particle_event.name, integer_event_handler)
            elif particle_event.event_type == ParticleDeviceEvent.EventType.STRING:
                get_particle_cloud().devices[self.name].subscribe(particle_event.name, string_event_handler)


    def get_variable_value(self, variable_name:str, refresh_values: bool=True):
        return get_particle_cloud().devices[self.name].variable(variable_name)

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

class ParticleDeviceEvent(TimeStampMixin):
    name = models.CharField(max_length=512, blank=True, null=True)
    persist_values = models.BooleanField(default=False)
    subscribe = models.BooleanField(default=False)
    device = models.ForeignKey(ParticleDevice, null=False, blank=False, on_delete=models.CASCADE, related_name='device_events')

    class EventType(models.IntegerChoices):
        FLOAT = 0
        INTEGER = 1
        STRING = 2

    event_type = models.IntegerField(choices=EventType.choices, default=EventType.STRING)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}|{self.event_type}"
