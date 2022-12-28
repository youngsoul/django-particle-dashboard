from django.contrib import admin
from .models import WeatherManager, WEATHER_MANAGER_SINGLETON_PK
from weather_readings.models import WeatherReading
import requests
from threading import Event, Thread
import time
import logging

app_logger = logging.getLogger("myapp")

_weather_thread: Thread = None
_weather_stop_event: Event = None


def _read_temperature_wind(weather_url):
    res = requests.get(weather_url)
    app_logger.debug(f"Read Temp/Wind: {weather_url}")
    app_logger.info(res.content)
    temp_data = res.json()
    t = temp_data['main']['temp']
    w = temp_data['wind']['speed']
    return t, w


def _get_new_weather_data(weather_stop_event):
    app_logger.debug(f'Get New Weather Data')
    continue_forever = True
    weather_manager = None
    while continue_forever:
        weather_manager = WeatherManager.objects.get(pk=WEATHER_MANAGER_SINGLETON_PK)
        for _ in range(0, weather_manager.polling_seconds // 5):
            time.sleep(5)  # 5 seconds, 5 minutes total
            if weather_stop_event.is_set():
                app_logger.warning(f"Weather Stop Event is Set")
                continue_forever = False
                break
        url = weather_manager.api_url + weather_manager.api_key
        if weather_manager.polling_enabled:
            try:
                temp, wind = _read_temperature_wind(url)
                weather_reading = WeatherReading()
                weather_reading.temp = temp
                weather_reading.wind = wind
                weather_reading.save()
                app_logger.info(f"weather: T:{temp}, W:{wind}")
            except Exception as Argument:
                app_logger.exception("Could not read Time/Wind values from API")

    if weather_manager:
        weather_manager.background_polling_running = False
        weather_manager.save()

    app_logger.warning(f"Leaving thread that gets to weather data.")


def _start_weather_readings():
    global _weather_stop_event, _weather_thread
    app_logger.info(f"Start weather readings")

    if _weather_thread is None:
        weather_manager = WeatherManager.objects.get(pk=WEATHER_MANAGER_SINGLETON_PK)
        if weather_manager:
            _weather_stop_event = Event()
            _weather_thread = Thread(target=_get_new_weather_data, args=(_weather_stop_event,))
            _weather_thread.daemon = True
            _weather_thread.start()
            weather_manager.background_polling_running = True
            weather_manager.save()
            app_logger.info("Weather readings started")
    else:
        app_logger.info(f"Weather thread already running")

def _stop_weather_readings():
    global _weather_thread
    # weather is a singleton so I know there is only one
    if _weather_stop_event is not None:
        _weather_stop_event.set()
        _weather_thread = None
        app_logger.info("Stop weather readings")


# Register your models here.
class WeatherManagerAdmin(admin.ModelAdmin):
    model = WeatherManager
    actions =['start_weather_readings', 'stop_weather_readings']

    def start_weather_readings(self, request, queryset):
        _start_weather_readings()

    def stop_weather_readings(self, request, queryset):
        _stop_weather_readings()

admin.site.register(WeatherManager, WeatherManagerAdmin)
