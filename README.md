# Deployment

"deploy":

    docker-compose up

start dev containers:

    docker-compose up api worker

view architecture with c4 diagrams:

    docker-compose up c4_models

start admin filler:

    docker-compose up internal

run manual update for all installations:

    docker exec -it energy-internal-1 python -c "from app.internal.admin import main; main()"


# [C4 Models](http://localhost:4444)

software architecture in c4 notation, its not dynamic so please changes the model (the .dsl file) with any major design changes.

# [Energy dashboard](http://localhost:5555)

flower UI for celery workers and tasks

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


## Alembic

write (local) database migrations:

    alembic revision --autogenerate -m "description"

if migration script is tested, rerun docker-compose, this updates the database with the latest migration version.
