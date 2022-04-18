# guiaMe
Automated Guiding Robot

## `docker-compose up --build`
Build the docker images and starts the front and back services

## Frontend
* Wait until you see ` Freezing container. Execute in container "yarn start"`
* Run in a new terminal `docker-compose exec frontend yarn start`

## Backend
* Wait until you see ` Freezing container. Execute in container "python manage.py runserver 0.0.0.0:8000"`
* Run in a new terminal `docker-compose exec backend python manage.py runserver 0.0.0.0:8000`

### Start only backend
* `docker-compose up -f docker-compose-back.yml --build`
* Wait until you see ` Freezing container. Execute in container "python manage.py runserver 0.0.0.0:8000"`
* Run in a new terminal `docker-compose exec backend python manage.py runserver 0.0.0.0:8000`

### Migrate and makemigrations
With the backend container up execute:
* `docker-compose exec backend python manage.py makemigrations`
* `docker-compose exec backend python manage.py migrate`

### Delete all volumes
Helps when the db changed
* `docker-compose down -v`