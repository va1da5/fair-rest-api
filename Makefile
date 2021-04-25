.PHONY: help user  run load_fixtures reload migrate

help:
	@echo "Usage:"
	@echo "  users              : creates user accounts"
	@echo "  run                : starts development server"
	@echo "  migrate            : creates and performs database migrations"
	@echo "  load_fixtures      : loads fixtures"
	@echo "  reload             : reloads development environment"

users:
	echo "from django.contrib.auth import get_user_model; \
	User = get_user_model();\
	User.objects.create_superuser('admin', 'admin@fair.com', 'password');\
	User.objects.create_user('alice', 'alice@mail.com', 'alice');\
	User.objects.create_user('bob', 'bob@mail.com', 'bob');\
	User.objects.create_user('emma', 'emma@inbox.com', 'emma');\
	User.objects.create_user('mark', 'mark@inbox.com', 'mark');\
	User.objects.create_user('ben', 'ben@inbox.com', 'ben');\
	"| python manage.py shell

run:
	@. .venv/bin/activate; \
	python manage.py runserver

migrate:
	python manage.py makemigrations;\
	python manage.py migrate;


load_fixtures:
	python manage.py loaddata --app household household.json
	python manage.py loaddata --app tasks task.json
	python manage.py loaddata --app core django_celery_beat.json

reload:
	@. .venv/bin/activate;\
	rm -rf db.sqlite3 fair/users/migrations/0* fair/tasks/migrations/0* fair/queue/migrations/0* fair/household/migrations/0*;\
	make migrate;\
	make users;\
	make load_fixtures

dumpdata:
	@. .venv/bin/activate;\
	python manage.py dumpdata household > fair/household/fixtures/household.json;\
	python manage.py dumpdata tasks > fair/tasks/fixtures/task.json;\
	python manage.py dumpdata queue > fair/queue/fixtures/queue.json;\
	python manage.py dumpdata django_celery_beat > fair/core/fixtures/django_celery_beat.json;

restart:
	docker-compose rm -sf api worker beats
	docker-compose up -d api worker beats
