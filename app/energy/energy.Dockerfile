FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY energy/pyproject.toml energy/poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11
 
WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY energy /code/app
COPY database /code/app
COPY core /code/app


CMD bash -c "watchmedo auto-restart -d app/ -p '*.py' --recursive -- celery -A app.energy.worker.celery worker --concurrency=1 --loglevel=info"