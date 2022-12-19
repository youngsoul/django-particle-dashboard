from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser, UsersParticleDevice


# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "particle_devices/dashboard.html"

    def get_context_data(self, **kwargs):
        original_data = super().get_context_data(**kwargs)
        my_devices = UsersParticleDevice.objects.filter(person=self.request.user)
        for user_device in my_devices:
            device = user_device.device
            device.particle_refresh()
            if not device.online:
                continue
            var_names = device.get_variable_names()
            var_values = []
            for var_name in var_names:
                try:
                    vval = device.get_variable_value(var_name)
                    print(var_name, vval)
                    var_values.append([var_name, vval])
                except:
                    pass
            device.variable_data = var_values
            print(device.name)

        original_data['users_devices'] = my_devices
        return original_data


