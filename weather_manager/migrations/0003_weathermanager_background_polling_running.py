# Generated by Django 4.1.4 on 2022-12-19 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_manager', '0002_weathermanager_api_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='weathermanager',
            name='background_polling_running',
            field=models.BooleanField(default=False),
        ),
    ]