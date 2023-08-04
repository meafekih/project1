python3 -m venv env
source env/bin/activate
pip install django
pip install graphene-django
django-admin startproject core .
django-admin startapp my_app

# settings.py
add my_app to INSTALLED_APPS
add in apps file: name = 'apps.crm'
add Query and mutation to core/schema.py
code .

# delete app
set app folder in trash
delete related app "query and mutation" from core/schema.py

complete libreary fonctionnaliy ( )
configure admin page
models.py attributes ..
search case using wrapper
complete authentication module
add test 
upload file image


