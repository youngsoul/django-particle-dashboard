from django.db import models
from typing import Dict
from datetime import datetime
from django.db import connection

average_query ="""with s as ( 
                    select float_value
                    from particle_readings_particlereading
                    where device_id=%s and event_name=%s
                    order by created_at desc
                    limit 3
                    )
                    select avg(float_value) from s;
                    """

# Create your models here.
class ParticleReading(models.Model):
    device_id = models.CharField(max_length=64, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at_utc = models.DateTimeField()
    float_value = models.FloatField(null=True, blank=True)
    int_value = models.FloatField(null=True, blank=True)
    str_value = models.CharField(max_length=512, null=True, blank=True)
    event_name = models.CharField(max_length=512, blank=True, null=True)

    # https://docs.djangoproject.com/en/4.1/topics/db/sql/
    def _get_average_float_value(self, device_id: str, event_name: str):
        average_float_value = None
        with connection.cursor() as cursor:
            cursor.execute(average_query, [device_id, event_name])
            row = cursor.fetchone()
            if row and row[0] is not None:
                average_float_value = float(row[0])
        return average_float_value

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
                average_float_value = self._get_average_float_value(device_id=device_id,
                                                                    event_name=event_data['event_name'])

                # calculate the percent change, and if the data_value is greater that 10% different
                # assume this is an anomoly ( we see single value spikes from time to time )
                # and instead of using the data_value use the average
                if average_float_value is not None:
                    pct_change = abs(float(data_value)-average_float_value)/average_float_value
                    # print(f"float values: {data_value}, {average_float_value}, {pct_change}")

                    if pct_change > 10.0:
                        data_value = average_float_value

                self.float_value = float(data_value)
            elif data_value_type == 1:
                self.int_value = int(data_value)
            elif data_value_type == 2:
                self.str_value = data_value

            self.published_at_utc = published_at_ts
            self.event_name = event_data['event_name']
        except Exception as exc:
            print(exc)

