FROM python:3.8-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN echo "\n Using user: $(whoami) \n"

FROM base as system_deps

RUN apt update -y && apt upgrade -y
RUN pip install --upgrade pip


FROM system_deps as python_deps
RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv install --system --deploy

FROM python_deps as runtime

WORKDIR /usr/app
