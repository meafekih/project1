from typing import Iterable, Optional
import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import auth_required, filter_resolver, email_duplicate, required_fields
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base
from graphql_auth import relay as graphql_auth_relay


class Customer(base):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=20)
    address = models.TextField()
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

    @auth_required
    @filter_resolver(CustomerType)
    def resolve_customers(self, info, **kwargs):
        print(settings.LIMIT_CHARS)
        return Customer.objects.all()
    
    def resolve_total_count(self, info):
        # Return the 'total_count' by invoking the custom method from MyModelConnection
        return CustomerConnection().total_count(info)

   

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
  
class UpdateCustomer(graphene.Mutation):   
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        email= graphene.String()
        phone = graphene.String()
        address= graphene.String()

    customer = graphene.Field(CustomerType)
    
    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            first_key, first_value = kwargs.popitem()
            if first_key=='id':
                customer = Customer.objects.filter(pk=first_value)
            else:
                filter_condition = {first_key: first_value}
                customer = Customer.objects.filter(**filter_condition)
                
            customer.update(**kwargs)
            return UpdateCustomer(customer=customer)
        except Exception as e:
            print(e)
        return None

class DeleteCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        email= graphene.String()
        phone = graphene.String()
        address= graphene.String()

    success = graphene.Boolean()
    
    def mutate(self, info, **kwargs):
        try:
            customer = Customer.objects.filter(**kwargs)
            count =  len(customer)
            if count ==0:
                raise('No instance')
            if count>1:
                raise('many instance')
            else:
                customer.delete()      
                return DeleteCustomer(success=True)
        except BaseException as e:
            print(e)
        return DeleteCustomer(success=False)
 
 