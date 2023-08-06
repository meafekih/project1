from django.contrib import admin

from .schemas.customer import Customer
admin.site.register(Customer)

from .schemas.contact import Contact
admin.site.register(Contact)

from .schemas.opportunity import Opportunity
admin.site.register(Opportunity)

from .schemas.task import Task
admin.site.register(Task)

from .schemas.product import Product
admin.site.register(Product)

from .schemas.sale import Sale
admin.site.register(Sale)

from .schemas.meeting import Meeting
admin.site.register(Meeting)

from .schemas.lead import Lead
admin.site.register(Lead)



"""
from django.apps import apps
app = apps.get_app_config('crm')

for model_name, model in app.models.items():
    admin.site.register(model)

from apps.crm.models import Product
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','description']
admin.site.register(Product, ProductAdmin)


"""

