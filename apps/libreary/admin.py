from django.contrib import admin
from django.apps import apps

""" 
from .models import  Author, Category, Publisher ,Book,BookInstance
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Publisher)
admin.site.register(BookInstance)
"""

app = apps.get_app_config('libreary')

for model_name, model in app.models.items():
    admin.site.register(model)



