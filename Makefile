setup: down build up-d migrate

build:
	docker-compose build

up:
	docker-compose up

up-d:
	docker-compose up -d

down:
	docker-compose down

shell:
	docker-compose run web sh

logs:
	docker-compose logs

migrate:
	docker-compose exec web python3 manage.py migrate