.PHONY: build start stop restart migrations migrate superuser

build:
	docker-compose build

start:
	docker-compose up

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
