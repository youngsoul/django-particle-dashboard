from django.db import models


# Create your models here.
class WeatherReading(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    temp = models.FloatField(null=True, blank=True)
    wind = models.IntegerField(null=True, blank=True)
