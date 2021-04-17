.PHONY: user  run load_tasks reload

users:
	echo "from django.contrib.auth import get_user_model; \
	User = get_user_model();\
	User.objects.create_superuser('admin', 'admin@myproject.com', 'password');\
	User.objects.create_user('alice', 'alice@myproject.com', 'alice');\
	User.objects.create_user('bob', 'bob@myproject.com', 'bob');\
	" | python manage.py shell

run:
	@. .venv/bin/activate; \
	python manage.py runserver

load_tasks:
	python manage.py loaddata --app tasks tasks.json

reload:
	@. .venv/bin/activate;\
	rm -rf db.sqlite3 fair/users/migrations/0* fair/tasks/migrations/0*;\
	python manage.py makemigrations;\
	python manage.py migrate;\
	make users;\
	make load_tasks
