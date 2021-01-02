help:
	@echo "all                    Build and run migrations"
	@echo "init                   all, then create a superuser"
	@echo "build				  Build the docker stack"
	@echo "clean                  Clean out the .pyc files"
	@echo "up                     Start all docker services in background"
	@echo "down                   Shut down all services"
	@echo "shell                  Start an IPython shell session"
	@echo "test                   Run the test suite"
	@echo "logs                   Tail the logs"
	@echo "check_flake8           check code quality via flake8"
	@echo "superuser              Create a superuser"
	@echo "migrate                Run database migrations"
	@echo "migrations [APP=app]   Make database migrations"
	@echo "fix_file_perm		  Grant permission to file created in docker shell"


all: clean build migrate

init: all superuser


clean:
	find . -name "*.pyc" -delete

build:
	docker-compose -f docker-compose-local.yml up --build -d

up:
	docker-compose -f docker-compose-local.yml up -d

down:
	docker-compose -f docker-compose-local.yml down

shell:
	docker-compose -f docker-compose-local.yml run django python manage.py shell

sh:
	docker-compose -f docker-compose-local.yml exec django bash

test:
	docker-compose -f docker-compose-local.yml exec django python manage.py test ${CASE} -v 2

logs:
	docker-compose -f docker-compose-local.yml logs -f

check_flake8:
	pip install flake8
	flake8

migrate:
	docker-compose -f docker-compose-local.yml run django python manage.py migrate

migrations: clean
	docker-compose -f docker-compose-local.yml run django python manage.py makemigrations ${APP}

collectstatic:
	docker-compose -f docker-compose-local.yml run django python manage.py collectstatic --noinput

superuser:
	docker-compose -f docker-compose-local.yml run django python manage.py createsuperuser

prod_deploy: guard-pem guard-host
	rsync -av -e "ssh -i ${pem}" . ${host}:~/var/www/django_app/
	ssh -i ${pem} ${host} "cd app/ && docker-compose -f docker-compose-production.yml up -d --build"

guard-%:
	@ if [  -z '${${*}}' ]; then echo 'variable $* not set' && exit 1; fi

	docker-compose -f docker-compose-local.yml exec django python manage.py createsuperuser

fix_file_perm:
	sudo chown -R $USER:$USER .
