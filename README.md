# app-lib

## Setup

docker-compose build
docker-compose up
docker-compose exec web python3 manage.py migrate
python3 manage.py createsuperuser

## Commands

python3 manage.py runserver
python3 manage.py makemigrations
python3 manage.py migrate

<!-- to create admin user -->

### apps

apps are little components that handle specific features (users..)
applib -> main app
python3 manage.py startapp base
