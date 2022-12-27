from django.contrib import admin
from .models import ParticleDevice, ParticleDeviceEvent
from accounts.models import UsersParticleDevice
import logging

app_logger = logging.getLogger('myapp')

# Register your models here.
class UserParticlesDevicesInLine(admin.StackedInline):
    model = UsersParticleDevice


class ParticleDeviceEventInline(admin.TabularInline):
    model = ParticleDeviceEvent


class ParticleDeviceAdmin(admin.ModelAdmin):
    model = ParticleDevice
    inlines = (UserParticlesDevicesInLine, ParticleDeviceEventInline)
    actions = ['refresh_particle_data', 'update_event_subscription']

    # https://stackoverflow.com/questions/5569091/django-admin-add-inlines-dynamically
    def get_inline_instances(self, request, obj=None):
        _inlines = super().get_inline_instances(request, obj=None)
        # custom_inline = YourDynamicInline(self.model, self.admin_site)
        # _inlines.append(custom_inline)
        app_logger.debug("******* CUSTOM INLINE INSTANCES")
        return _inlines

    def update_event_subscription(self, request, queryset):
        app_logger.debug("update event subscription")

        for device in queryset:
            for particle_event in device.device_events.all():
                app_logger.debug(f"event: {particle_event}")
                device.update_event_subscription(particle_event)

    def refresh_particle_data(self, request, queryset):
        app_logger.debug("refresh particle data")
        for device in queryset:
            device.particle_refresh()

    refresh_particle_data.short_description = "Refresh Particle Data"


admin.site.register(ParticleDevice, ParticleDeviceAdmin)
