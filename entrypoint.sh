#! /bin/bash



echo Appling Database migrations.
python manage.py makemigrations --noinput
python manage.py migrate --noinput


echo Creating super user
python manage.py createsu

echo Collecting static
python manage.py collectstatic --noinput


# specify executor specific command
exec "$@"
