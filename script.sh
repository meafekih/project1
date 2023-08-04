python3 -m venv env
source env/bin/activate
pip install django
pip install graphene-django
django-admin startproject core .
django-admin startapp my_app

# settings.py
add my_app to INSTALLED_APPS
code .

