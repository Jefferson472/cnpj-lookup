django-run:
	python src/manage.py runserver --settings=setup.settings.local

django-migrate:
	python src/manage.py makemigrations --settings=setup.settings.local
	python src/manage.py migrate --settings=setup.settings.local
