from django.contrib import admin
from .models import ParticleDevice
from accounts.models import UsersParticleDevice
from .utils import get_particle_cloud
from pyparticleio.ParticleCloud import ParticleCloud

# Register your models here.
class UserParticlesDevicesInLine(admin.StackedInline):
    model = UsersParticleDevice

class ParticleDeviceAdmin(admin.ModelAdmin):
    model = ParticleDevice
    inlines = (UserParticlesDevicesInLine,)
    actions = ['refresh_particle_data']

    def refresh_particle_data(self, request, queryset):
        print("refresh particle data")
        for device in queryset:
            device.particle_refresh()

    refresh_particle_data.short_description = "Refresh Particle Data"

admin.site.register(ParticleDevice, ParticleDeviceAdmin)
