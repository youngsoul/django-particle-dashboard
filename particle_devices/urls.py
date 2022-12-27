from django.urls import path
from .views import DevicesView

urlpatterns = [
    path("", DevicesView.as_view(), name="devices"),

]