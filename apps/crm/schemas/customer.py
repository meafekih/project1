import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import (auth_required, filter_resolver,
     email_duplicate, required_fields, unique_instance, download)
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base
from django import forms
from apps.authentication.models import ExtendUser as User
import datetime
import asyncio
import base64
from django.core.files.base import ContentFile
from datetime import datetime as dt


class Customer(base):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user', null=True) # it means that the field is allowed to be left blank 

    document = models.FileField(upload_to='crm/')
    description = models.CharField(max_length=255, blank=True)# it means that the field is allowed to have a NULL value in the database. It applies to database storage.
    
    def __str__(self):
        return self.name

    def save(self, ) -> None:
        # Perform custom logic before saving
        self.address = self.address.upper()
        return super().save()

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'



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

    download_image = graphene.Field(CustomerType,)
    #filename=graphene.String(required=True))

    def resolve_total_count(self, info):
        print(settings.LIMIT_CHARS)
        return CustomerConnection().total_count(info)
    
    @filter_resolver(CustomerType)
    def resolve_download_image(self, info, name, **kwargs):
        try:
            #image_file = Customer.objects.get(file_name=filename)      
            # image_file.file.url 
            customer = Customer.objects.filter(**kwargs)
            count = len(customer)
            print('count ' + count)
            return 'file.png'
        except Customer.DoesNotExist:
            return None

    #@auth_required
    @filter_resolver(CustomerType)
    def resolve_customers(self, info, **kwargs):
        #qs = Customer.objects.filter(name='34')  
        qs = Customer.objects.exclude(created_at__gt=datetime.date(2023, 1, 3), name="34")
        #SELECT ... WHERE NOT (created_at > '2005-1-3' AND name = '34')

        qs =Customer.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3)).exclude(name="34")
        #SELECT ...WHERE NOT pub_date > '2005-1-3' AND NOT headline = 'Hello'


        print(qs)
        return qs
   
    
""" 
class InsertCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email= graphene.String()
        phone = graphene.String()
        address= graphene.String()
        description = graphene.String()
        files_names = graphene.String() 
        files = graphene.String()  # Base64-encoded image data
    customer = graphene.Field(CustomerType)
    
    @email_duplicate(Customer) # must authenticate to save user
    @required_fields('name', 'email')
    def mutate(self, info, **kwargs):

        files_names = kwargs.pop('files_names', None)
        files = kwargs.pop('files', None)
        customer = Customer( **kwargs)
        user = User.objects.get(username=str(info.context.user))
        setattr(customer, "created_by", user)  
        customer.save()      
        return InsertCustomer(customer=customer)
    
"""

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
        #file_name = graphene.String()
        #file = graphene.String()  # Base64-encoded image data

    customer = graphene.Field(CustomerType)

    def mutate(self, info, parameter, value, **kwargs):
        lookup_kwargs = {parameter: value}
        customer_query = Customer.objects.filter(**lookup_kwargs)
        print(customer_query)
        file_name= "_"; image_data=None
        for customer in customer_query:
        # this for all instances filter 
        # if you want get just first inscance delete prevuious for
            for field_name, field_value in kwargs.items():                
                    setattr(customer, field_name, field_value)                
            customer.save()
        return UpdateCustomer(customer=customer)

class ShowTime(graphene.ObjectType):
    showTime = graphene.String()

    async def subscribe_showTime(root, info):
        while True:
            yield dt.now().isoformat()
            await asyncio.sleep(1)




class InsertCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email= graphene.String()
        phone = graphene.String()
        address= graphene.String()
        file_name = graphene.String()
        file = graphene.String()

    customer = graphene.Field(CustomerType)

    @email_duplicate(Customer) # must authenticate to save user
    @required_fields('name', 'email')
    def mutate(self, info, **kwargs):
        customer = Customer()
        file_name = kwargs.pop('files_names', None)
        file = kwargs.pop('files', None)
        if file_name:
            file_name= kwargs.get('file_name')
        if file:
            image_data = base64.b64decode(kwargs.get('file'))
            customer.document.save(file_name , ContentFile(image_data))        
        customer = Customer( **kwargs)
        customer.save()


        return InsertCustomer(customer=customer)



""" 
class InsertCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email= graphene.String()
        phone = graphene.String()
        address= graphene.String()
        file_name = graphene.String()
        file = graphene.String()

    customer = graphene.Field(CustomerType)

    @email_duplicate(Customer) # must authenticate to save user
    @required_fields('name', 'email')
    def mutate(self, info, **kwargs):
        customer = Customer()
        file_name= ""; image_data=None
        for field_name, field_value in kwargs.items():
            if (field_name=='file'):
                file = kwargs.get('file')
                image_data = base64.b64decode(file)
            if field_name=='file_name':
                file_name= kwargs.get('file_name')
            setattr(customer, field_name, field_value)
        if image_data:
            customer.document.save(file_name , ContentFile(image_data))
        customer.save()
        return InsertCustomer(customer=customer)

 """

"""
import base64
from django.core.files.base import ContentFile
class UpdateCustomer(graphene.Mutation):
    class Arguments:
        parameter = graphene.String(required=True)
        value = graphene.String(required=True)
        name = graphene.String()
        email= graphene.String()
        phone = graphene.String()
        address= graphene.String()
        file_name = graphene.String()
        file = graphene.String()  # Base64-encoded image data

    customer = graphene.Field(CustomerType)

    def mutate(self, info, parameter, value, **kwargs):
        lookup_kwargs = {parameter: value}
        customer_query = Customer.objects.filter(**lookup_kwargs)
        file_name= "_"; image_data=None
        for customer in customer_query:
        # this for all instances filter 
        # if you want get just first inscance delete prevuious for
            for field_name, field_value in kwargs.items():
                if (field_name!='file') & (field_name!='file_name'):
                    setattr(customer, field_name, field_value)
                if (field_name=='file'):
                    file = kwargs.get('file')
                    image_data = base64.b64decode(file)
                if field_name=='file_name':
                    file_name= kwargs.get('file_name')
            if image_data:
                customer.file.save(file_name + '.png', ContentFile(image_data))
            customer.save()
        return UpdateCustomer(customer=customer)

"""



