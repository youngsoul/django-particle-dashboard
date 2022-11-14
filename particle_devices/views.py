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

        original_data['users_devices'] = my_devices
        return original_data


