import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import auth_required, filter_resolver, email_duplicate
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base


class Customer(base):
    name = models.CharField(max_length=100)
    email = models.EmailField()
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
    customer = graphene.Field(CustomerType)
    
    @classmethod
    @email_duplicate
    def mutate(cls, root, info, name, email):
        print(settings.LIMIT_CHARS)
        customer = Customer(name=name, email=email)
        customer.save()      
        return InsertCustomer(customer=customer)

