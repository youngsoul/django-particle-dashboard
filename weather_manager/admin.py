from django.contrib import admin
from .models import WeatherManager, WEATHER_MANAGER_SINGLETON_PK
from weather_readings.models import WeatherReading
import requests
from threading import Event, Thread
import time

_weather_thread: Thread = None
_weather_stop_event: Event = None


def _read_temperature_wind(weather_url):
    res = requests.get(weather_url)
    temp_data = res.json()
    t = temp_data['main']['temp']
    w = temp_data['wind']['speed']
    return t, w


def _get_new_weather_data(weather_stop_event):
    continue_forever = True
    weather_manager = None
    while continue_forever:
        weather_manager = WeatherManager.objects.get(pk=WEATHER_MANAGER_SINGLETON_PK)
        for _ in range(0, weather_manager.polling_seconds // 5):
            time.sleep(5)  # 5 seconds, 5 minutes total
            if weather_stop_event.is_set():
                continue_forever = False
                break
        url = weather_manager.api_url + weather_manager.api_key
        if weather_manager.polling_enabled:
            temp, wind = _read_temperature_wind(url)
            weather_reading = WeatherReading()
            weather_reading.temp = temp
            weather_reading.wind = wind
            weather_reading.save()

    if weather_manager:
        weather_manager.background_polling_running = False
        weather_manager.save()


# Register your models here.
def start_weather_readings(modeladmin, request, queryset):
    global _weather_stop_event, _weather_thread

    if _weather_thread is None:
        weather_manager = WeatherManager.objects.get(pk=WEATHER_MANAGER_SINGLETON_PK)
        if weather_manager:
            _weather_stop_event = Event()
            _weather_thread = Thread(target=_get_new_weather_data, args=(_weather_stop_event,))
            _weather_thread.daemon = True
            _weather_thread.start()
            weather_manager.background_polling_running = True
            weather_manager.save()


def stop_weather_readings(modeladmin, request, queryset):
    global _weather_thread
    if _weather_stop_event is not None:
        _weather_stop_event.set()
        _weather_thread = None


# Register your models here.
class WeatherManagerAdmin(admin.ModelAdmin):
    pass


admin.site.register(WeatherManager, WeatherManagerAdmin)
admin.site.add_action(start_weather_readings, "Start Weather Readings")
admin.site.add_action(stop_weather_readings, "Stop Weather Readings")
