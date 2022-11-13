# Simple Sample Django4 Docker Project Starter

The goal of this repo is to create an Django4.x/Postgres docker environment without you having to create a local python virtual environment.  The virtual environment will be created in the image and the running container from the image.  

This repo assumes you have Docker installed and can issue docker and docker-compose commands from a terminal window.

To add new Python dependencies, update the requirements.in file, and rebuild the image.

### pip-tools
This docker image uses `pip-tools` to manage dependencies.  By placing the dependent module name with an optional version in the `requirements.in` file, the module and its dependencies will be installed into the Python virtual environment of the container.


## Setup


* clone this repo and in terminal window run:

```shell
git clone https://github.com/youngsoul/sample-django4-docker-project-starter.git <projectdirname>
```

* Open docker-compose.yml and change the container_name fields to be something relevant to the project

* Open Makefile and at the top, update the container names to match

* make init-project

Run the make target `init-project`.
This will call the `django-admin startproject` command in the django web container

Note that this will NOT run an initial migration because we want to create a custom User model BEFORE we run the initial migration.

```shell
make init-project
```

* Update django_project/settings.py to include 'accounts' app

## PyCharm

You can now create a PyCharm project and set the Python Interpreter to the docker-compose.yml files selecting 'django-web' as the service

This will keep you from having to create a local venv just to install Django and call startproject.

## Settings.py

```python
from environs import Env # new
env = Env() # new

env.read_env() # new

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG")

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")


DATABASES = {
"default": env.dj_db_url("DATABASE_URL", default=env("DATABASE_URL"))
}
```



## Start the Containers

```shell
make run
```

You can open a browser and go to:

http://localhost:8000

and you should see the familiar Django start page.


## Custom User model

You almost always want to create a customer user model, BEFORE your initial migration.

* Create a CustomUser model
* Update django_project/settings.py
* Customize UserCreationForm and UserChangeForm
* Add the custom user model to admin.py

```shell
make startapp appname=accounts
```

See `accounts_starter_files` directory for what the simple CustomUser model looks like.

As an example,
```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    pass
```

* settings.py

```python
# django_project/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local
    "accounts"
]

# at the bottom of the file
AUTH_USER_MODEL = "accounts.CustomUser"
```

* Make migrations

```shell
make migrations appname=accounts
```

* Run migrations

```shell
make migrate
```

* Create Superuser

```shell
make superuser
```
