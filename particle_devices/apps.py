from django.apps import AppConfig
import logging

app_logger = logging.getLogger('myapp')

class ParticleDevicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'particle_devices'

    def ready(self):
        from .models import ParticleDevice
        app_logger.debug("Running Particle Device App Config Ready")
        for device in ParticleDevice.objects.all():
            for particle_event in device.device_events.all():
                device.update_event_subscription(particle_event)
                app_logger.debug(f"Suscribe to event: {particle_event} for device: {device.device_id}")

