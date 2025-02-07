#!/bin/bash

echo "Aplicando migrações..."
python manage.py makemigrations
python manage.py migrate

echo "Iniciando o servidor..."
gunicorn core.wsgi:application
