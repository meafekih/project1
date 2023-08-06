import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import auth_required, email_duplicate
from .models import (Customer, Contact, Opportunity, Task,
    Product, Sale, Meeting, Lead)
from .types import (CustomerType, ContactType, OpportunityType, TaskType,
    ProductType, SaleType, MeetingType, LeadType,
    ProductConnection, ContactsConnection)
from django.conf import settings
from graphene import relay
from apps.base.decorators import filter_resolver

# add upload_file 
from graphene_file_upload.scalars import Upload

# Customer

class Customers(graphene.ObjectType):
    customers = graphene.List(CustomerType,#id=graphene.ID(),name=graphene.String())
    **{field: graphene.Argument(graphene.String) for field in CustomerType._meta.fields})

    @auth_required
    @filter_resolver(CustomerType)
    def resolve_customers(self, info, **kwargs):
        print(info.context.user)
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


# Contact

class Contacts(graphene.ObjectType):
    contacts = relay.ConnectionField(ContactsConnection, #)
    **{field: graphene.Argument(graphene.String) for field in ContactType._meta.fields})

    @auth_required
    @filter_resolver(ContactType)
    def resolve_contacts(self, info, **kwargs):     
        contacts = Contact.objects.all()
        return contacts




# Product

class Products(graphene.ObjectType):
    products = relay.ConnectionField(ProductConnection)
    
    def resolve_products(self, info, **kwargs):     
        products = Product.objects.all()
        return products



from .schemas.campaign import Campaigns
class Query(Customers, Products, Contacts, Campaigns ):
    pass

class Mutation(graphene.ObjectType):
    insertCustomer = InsertCustomer.Field()


