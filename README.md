# ALR
Automated Leading Robot

## `docker-compose up --build`
Build the docker images and starts the front and back services

## Frontend
* Wait until you see ` Freezing container. Execute in container "yarn start"`
* Run in a new terminal `docker-compose exec frontend yarn start`

## Backend
* Wait until you see ` Freezing container. Execute in container "python manage.py runserver"`
* Run in a new terminal `docker-compose exec backend python manage.py runserver`
