# Pull base image
FROM python:3.10.4-slim-bullseye as base

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1

FROM base as builder

RUN apt-get update && apt-get -y upgrade && apt-get install --no-install-recommends -y \
  curl \
  zip \
  nano \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /code
RUN mkdir templates

# Install Dependencies
# copy local project code to container code
# first '.' is where the Dockerfile is, the second '.' is to the WORKDIR
COPY . .

RUN pip install pip-tools
RUN pip-compile requirements.in --upgrade

FROM builder as deployment

RUN pip-sync

RUN adduser --disable-password myuser
USER myuser

# run command to keep the container running
# override this command in docker-compose
# python manage.py runserver 0.0.0.0:8000
#CMD ["bash", "-c", "python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD gunicorn drf_project.wsgi:application --bind 0.0.0.0:$PORT

FROM builder as local_dev

ENV PYTHONDONTWRITEBYTECODE 1

RUN pip-compile requirements-dev.in --upgrade
RUN pip-sync requirements*.txt

# run command to keep the container running
# override this command in docker-compose
CMD ["bash", "-c", "tail", "/dev/null"]
