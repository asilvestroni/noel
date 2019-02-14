test:
	python manage.py test main.tests
lint:
	pylint main --rcfile=.pylint --load-plugins pylint_django
collect-static:
	python manage.py collectstatic --no-input
migrate:
	python manage.py makemigrations main
	python manage.py migrate --run-syncdb
compose-up:
	docker-compose -f docker/docker-compose.yml up -d
compose-down:
	docker-compose -f docker/docker-compose.yml down
compose-restart:
	docker-compose -f docker/docker-compose.yml down && docker-compose -f docker/docker-compose.yml up -d
docker-migrate:
	docker-compose -f docker/docker-compose.yml exec web python manage.py makemigrations && python manage.py migrate
docker-build:
	docker build -f docker/Dockerfile . -t noel