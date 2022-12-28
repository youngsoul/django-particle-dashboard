from django.apps import AppConfig
import logging


app_logger = logging.getLogger('myapp')

class WeatherManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather_manager'

    def ready(self):
        from .admin import _start_weather_readings
        app_logger.debug("Running Weather Manager App Config Ready")
        _start_weather_readings()


