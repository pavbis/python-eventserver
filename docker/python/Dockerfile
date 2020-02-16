FROM python:3.7-slim

RUN apt-get update && apt-get install -y \
      gcc gettext libpq-dev python-dev python-psycopg2 \
      git \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# We want output
ENV PYTHONUNBUFFERED 1
# We don't want *.pyc
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/

# Install pipenv
RUN pip3 install pipenv

# Copy Pipfiles in the container
COPY Pipfile Pipfile.lock ./

# Install app deps
RUN pipenv install -d