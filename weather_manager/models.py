from django.db import models

WEATHER_MANAGER_SINGLETON_PK = 1

# Create your models here.
class SingletonModel(models.Model):
    def save(self, *args, **kwargs):
        self.pk = WEATHER_MANAGER_SINGLETON_PK
        return super().save(*args, **kwargs)


class WeatherManager(SingletonModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    api_key = models.CharField(max_length=128, blank=True, null=True)
    polling_enabled = models.BooleanField(default=False)
    background_polling_running = models.BooleanField(default=False)
    polling_seconds = models.IntegerField(default=300)
    api_url=models.CharField(max_length=512, default="https://api.openweathermap.org/data/2.5/weather?lat=42.203010&lon=-88.119750&exclude=alerts,daily,hourly,minutely&units=imperial&appid=")
