# Generated by Django 4.1.3 on 2022-11-19 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('particle_devices', '0007_particledeviceevent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='particledeviceevent',
            old_name='persist_value',
            new_name='persist_values',
        ),
        migrations.AddField(
            model_name='particledeviceevent',
            name='activitly_monitor',
            field=models.BooleanField(default=False),
        ),
    ]