from django.contrib import admin
from django.apps import apps

 
app = apps.get_app_config('crm')

for model_name, model in app.models.items():
    admin.site.register(model)

"""
from apps.crm.models import Product
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','description']
admin.site.register(Product, ProductAdmin)
"""

