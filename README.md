# Deployment

<!-- create external volume for presist data between different docker projects

    docker volume create energy-database -->

start all docker containers with

    docker-compose up -d database pgadmin

    docker-compose up energy

# [Postgres admin interface](http://localhost:8080)

login:

- Email: admin@kieback-peter.nl
- Password: admin

click on 'add new server', go to connection tab:

- Hostname: database
- Username: super_kp
- Password: super_kp

# Dependencies

### Prerequisites

- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker-compose](https://docs.docker.com/compose/)

### Stack

- [Fast api](https://fastapi.tiangolo.com/) + Uvicorn
- [SQLAlchemy](https://sqlalchemy.org) + [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment) + Postgres

## Poetry

make sure you have poetry as package manager

install requirements

    poetry install

activate shell with dependencies:

    poetry shell

    deactivate

## Alembic

to write database migrations change DB_HOST in env to localhost and forward docker port to localhost in docker-compose:

    alembic revision --autogenerate -m "description"

if migration script is tested, undo above changes and rerun docker-compose, this updates the database with the latest migration version. Please do improve workflow :)
