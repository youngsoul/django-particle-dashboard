from typing import Dict
from particle_readings.models import ParticleReading


def float_event_handler(event_data: Dict):
    print(f"float event handler: {event_data}")
    try:
        if event_data is not None:
            particle_reading = ParticleReading()
            particle_reading.from_event_data(event_data, 0)
            particle_reading.save()
    except Exception as exc:
        print(exc)


def integer_event_handler(event_data: Dict):
    print(f"integer event handler: {event_data}")
    try:
        if event_data is not None:
            particle_reading = ParticleReading()
            particle_reading.from_event_data(event_data, 1)
            particle_reading.save()
    except Exception as exc:
        print(exc)


def string_event_handler(event_data: Dict):
    print(f"string event handler: {event_data}")
    try:
        if event_data is not None:
            particle_reading = ParticleReading()
            particle_reading.from_event_data(event_data, 2)
            particle_reading.save()
    except Exception as exc:
        print(exc)
