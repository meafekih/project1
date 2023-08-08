import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import (auth_required, filter_resolver,
     email_duplicate, required_fields, unique_instance, download)
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base
import base64



class Customer(base):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    file = models.ImageField(upload_to='images/') 
    
    def __str__(self):
        return self.name

    def save(self, ) -> None:
        # Perform custom logic before saving
        self.address = self.address.upper()
        return super().save()

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'
        interfaces = [relay.Node]# for pagination
    
    def resolve_name(self, info):
        # Perform custom logic on the 'name' field before returning to the client
        return self.name.upper()

class CustomerConnection(relay.Connection):
    class Meta:
        node = CustomerType     

    def total_count(self, info):
        # Perform custom logic to return the total count of MyModel objects
        return Customer.objects.count()



class Customers(graphene.ObjectType):
    customers = relay.ConnectionField(CustomerConnection, #)
    **{field: graphene.Argument(graphene.String) for field in CustomerType._meta.fields})
    total_count = graphene.Int()

    download_image = graphene.Field(CustomerType, filename=graphene.String(required=True))

    @auth_required
    @filter_resolver(CustomerType)
    def resolve_customers(self, info, **kwargs):
        print(settings.LIMIT_CHARS)
        return Customer.objects.all()
    
    def resolve_total_count(self, info):
        return CustomerConnection().total_count(info)
    
        #@download('path', 'filename')
    def resolve_download_image(self, info, filename):
        try:
            image_file = Customer.objects.get(name=filename)
            return image_file
        except Customer.DoesNotExist:
            return None



from django.core.files.base import ContentFile

class UploadImage(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        file = graphene.String()  # Base64-encoded image data

    image = graphene.Field(CustomerType)

    def mutate(self, info, name, file):
        image_data = base64.b64decode(file)
        image_file = Customer(name=name)
        image_file.file.save(name + '.png', ContentFile(image_data))
        image_file.save()
        return UploadImage(image=image_file)





















class InsertCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email= graphene.String()
        phone = graphene.String()
        address= graphene.String()
    customer = graphene.Field(CustomerType)
    
    @email_duplicate(Customer)
    @required_fields('name', 'email')
    def mutate(self, info, **kwargs):
        customer = Customer(**kwargs)
        customer.save()      
        return InsertCustomer(customer=customer)

class DeleteCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email= graphene.String()
        phone = graphene.String()
        address= graphene.String()

    success = graphene.Boolean()
    
    @unique_instance(Customer)
    def mutate(self, info, **kwargs):
        instance = Customer.objects.filter(**kwargs)
        instance.delete()
        return DeleteCustomer(success=True)
 
class UpdateCustomer(graphene.Mutation):
    class Arguments:
        parameter = graphene.String(required=True)
        value = graphene.String(required=True)
        name = graphene.String()
        email= graphene.String()
        phone = graphene.String()
        address= graphene.String()

    Output = CustomerType

    def mutate(self, info, parameter, value, **kwargs):
        update_handler = ModelUpdateHandler(parameter, value)
        Output = update_handler.update_model(**kwargs)
        return Output

class ModelUpdateHandler: # set this class genric for all classes
    def __init__(self, parameter, value):
        self.parameter = parameter
        self.value = value
   
    def update_model(self, **kwargs):
        lookup_kwargs = {self.parameter: self.value}
        matching_models = Customer.objects.filter(**lookup_kwargs)
        for model in matching_models:
            for field_name, field_value in kwargs.items():
                setattr(model, field_name, field_value)
            model.save()
        return matching_models



