from pyparticleio.ParticleCloud import ParticleCloud
import os

particle_cloud = None


def get_particle_cloud() -> ParticleCloud:
    global particle_cloud
    if particle_cloud is None:
        particle_cloud = ParticleCloud(username_or_access_token=os.getenv("PARTICLEIO_ACCESS_TOKEN"))

    return particle_cloud
