# pull official base image
FROM python:3.11.2-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./Pipfile* /usr/src/app/
RUN pip install pipenv
RUN pipenv install --skip-lock --system --dev --ignore-pipfile

# copy project
COPY . /usr/src/app/