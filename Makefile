.PHONY: build start stop restart migrations migrate superuser install

build:
	docker-compose build

start:
	docker-compose up

install:
	docker-compose exec web python3 -m pip install Pillow

stop:
	docker-compose down

restart:
	stop start
	
migrations:
	docker-compose exec web python3 manage.py makemigrations

migrate:
	docker-compose exec web python3 manage.py migrate


superuser:
	docker-compose exec web python3 manage.py createsuperuser

seeders:
	docker-compose exec web python3 manage.py loaddata base/fixtures/user.json
	docker-compose exec web python3 manage.py loaddata base/fixtures/topic.json
	docker-compose exec web python3 manage.py loaddata base/fixtures/room.json
	docker-compose exec web python3 manage.py loaddata base/fixtures/message.json
	docker-compose exec web python3 manage.py loaddata base/fixtures/collection.json
	docker-compose exec web python3 manage.py loaddata base/fixtures/genre.json
	docker-compose exec web python3 manage.py loaddata base/fixtures/book.json

