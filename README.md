# app-lib

## Setup

```bash
docker-compose build
```

```bash
docker-compose up
```

```bash
docker-compose python3 manage.py makemigrations
```

```bash
docker-compose exec web python3 manage.py migrate
```

```bash
docker-compose exec web python3 manage.py createsuperuser
```

## Commands

python3 manage.py runserver
python3 manage.py migrate
