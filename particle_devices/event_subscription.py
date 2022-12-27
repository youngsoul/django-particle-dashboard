from typing import Dict
from particle_readings.models import ParticleReading
import logging

app_logger = logging.getLogger("myapp")

def float_event_handler(event_data: Dict):
    app_logger.info(f"float event handler: {event_data}")

    try:
        if event_data is not None:
            particle_reading = ParticleReading()
            particle_reading.from_event_data(event_data, 0)
            particle_reading.save()
    except Exception as exc:
        app_logger.exception(exc)


def integer_event_handler(event_data: Dict):
    app_logger.info(f"integer event handler: {event_data}")
    try:
        if event_data is not None:
            particle_reading = ParticleReading()
            particle_reading.from_event_data(event_data, 1)
            particle_reading.save()
    except Exception as exc:
        app_logger.exception(exc)


def string_event_handler(event_data: Dict):
    app_logger.info(f"string event handler: {event_data}")
    try:
        if event_data is not None:
            particle_reading = ParticleReading()
            particle_reading.from_event_data(event_data, 2)
            particle_reading.save()
    except Exception as exc:
        app_logger.exception(exc)
