import pytest
from particle_devices.models import ParticleDevice
from accounts.models import UsersParticleDevice
from django.contrib.auth import get_user_model
from pyparticleio import ParticleCloud
from environs import Env

@pytest.mark.django_db
def test_particle_device():
    User = get_user_model()
    user1 = User.objects.create_user(username="user1", email="user1@example.com", password="test123@")
    pd = ParticleDevice(device_id="1234567890")
    pd.save()
    assert pd.device_id == "1234567890"

    pd2 = ParticleDevice(device_id="0987654321")
    pd2.save()
    assert pd2.device_id == "0987654321"

    ud = UsersParticleDevice(person=user1, device=pd)
    ud.save()

    ud2 = UsersParticleDevice(person=user1, device=pd2)
    ud2.save()

    assert ud.person == user1

    assert user1.particle_devices.count() == 2

    my_devices = UsersParticleDevice.objects.filter(person=user1)
    assert my_devices is not None
    assert len(my_devices) == 2

    users_of_device = UsersParticleDevice.objects.filter(device=pd)
    assert users_of_device is not None
    assert len(users_of_device) == 1
