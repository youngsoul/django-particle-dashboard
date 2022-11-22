from django.db import models
from typing import Dict
from datetime import datetime


# Create your models here.
class ParticleReading(models.Model):
    device_id = models.CharField(max_length=64, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at_utc = models.DateTimeField()
    float_value = models.FloatField(null=True, blank=True)
    int_value = models.FloatField(null=True, blank=True)
    str_value = models.CharField(max_length=512, null=True, blank=True)
    event_name = models.CharField(max_length=512, blank=True, null=True)

    def from_event_data(self, event_data: Dict, data_value_type: int):
        """
        data_value_type
                FLOAT = 0
                INTEGER = 1
                STRING = 2

        """
        try:
            device_id = event_data['coreid']
            data_value = event_data['data']
            published_at = event_data['published_at']
            published_at = published_at.replace('Z', "+00:00")
            published_at_ts = datetime.fromisoformat(published_at)

            self.device_id = device_id
            if data_value_type == 0:
                self.float_value = float(data_value)
            elif data_value_type == 1:
                self.int_value = int(data_value)
            elif data_value_type == 2:
                self.str_value = data_value

            self.published_at_utc = published_at_ts
            self.event_name = event_data['event_name']
        except Exception as exc:
            print(exc)

