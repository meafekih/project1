import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import auth_required, filter_resolver, email_duplicate
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base

class Customer(base):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    def __str__(self):
        return self.name

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'
        interfaces = [relay.Node]# for pagination

class CustomerConnection(relay.Connection):
    class Meta:
        node = CustomerType      




class Customers(graphene.ObjectType):
    customers = graphene.List(CustomerType,#id=graphene.ID(),name=graphene.String())
    **{field: graphene.Argument(graphene.String) for field in CustomerType._meta.fields})

    @auth_required
    @filter_resolver(CustomerType)
    def resolve_customers(self, info, **kwargs):
        return Customer.objects.all()

class InsertCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email= graphene.String(required=False)
        phone = graphene.String()
        address= graphene.String()


    customer = graphene.Field(CustomerType)
    
    @email_duplicate(Customer)
    def mutate(self, info, **kwargs):
        print(settings.LIMIT_CHARS)
        customer = Customer(**kwargs)
        customer.save()      
        return InsertCustomer(customer=customer)


""" 
class UpdateCustomer(graphene.Mutation):     
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        email = graphene.String()

    def mutate(self, info, id, name=None, email=None):
        try:
            customer = Customer.objects.get(pk=id)
            if name is not None:
                customer.name = name
            if email is not None:
                customer.email = email
            customer.save()

            return UpdateCustomer(success=True)
        except Customer.DoesNotExist:
            return UpdateCustomer(success=False)


class DeleteCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email= graphene.String()
        phone = graphene.String()
        address= graphene.String()

    success = graphene.Boolean()
    
    def mutate(self, info, **kwargs):
        try:
            customer = Customer.objects.get(**kwargs)
            customer.delete()      
            return InsertCustomer(success=True)
        except:
            pass
        return InsertCustomer(success=False)
 """