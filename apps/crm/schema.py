import graphene
from graphene_django.types import DjangoObjectType
from .decorators import auth_required, email_duplicate
from .models import (Customer, Contact, Opportunity, Task,
    Product, Sale, Meeting, Lead, Campaign)
from .types import (CustomerType, ContactType, OpportunityType, TaskType,
    ProductType, SaleType, MeetingType, LeadType, CampaignType,
    ProductConnection)
from django.conf import settings
from graphene import relay

# add upload_file 
from graphene_file_upload.scalars import Upload

# Customer

class Customers(graphene.ObjectType):

    customers = graphene.List(CustomerType,id=graphene.ID(),name=graphene.String())

    @auth_required
    def resolve_Permissions(self, info, id=None, name=None):
        print(info.context.user)
        queryset = Customer.objects.all()
        if id:
            queryset = queryset.filter(id=id)
        if name:
            queryset = queryset.filter(name=name)
        return queryset

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


# Product

class Products(graphene.ObjectType):
    products = relay.ConnectionField(ProductConnection)
    
    def resolve_products(self, info, **kwargs):     
        products = Product.objects.all()
        return products










class Query(Customers, Products, ):
    pass

class Mutation(graphene.ObjectType):
    insertCustomer = InsertCustomer.Field()


