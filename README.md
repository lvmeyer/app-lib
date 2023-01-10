# app-lib

## Setup

docker-compose build
docker-compose up
docker-compose python3 manage.py makemigrations
docker-compose exec web python3 manage.py migrate

python3 manage.py createsuperuser

## Commands

python3 manage.py runserver
python3 manage.py migrate
