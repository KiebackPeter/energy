FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11
 
WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY api /code/app
COPY database /code/app
COPY core /code/app
CMD bash -c "uvicorn api.main:api --proxy-headers --host 0.0.0.0  --header server:energy-portal --ssl-keyfile app/core/certificates/star_kieback-peter.net-decrypted.key --ssl-certfile app/core/certificates/star_kieback-peter.net.crt --reload"