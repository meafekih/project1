import graphene
from graphene_django.types import DjangoObjectType
from .models import (Customer, Contact, Opportunity, Task,
                    Product, Sale, Meeting, Lead, Campaign)

from .types import (CustomerType, ContactType, OpportunityType, TaskType,
                    ProductType, SaleType, MeetingType, LeadType, CampaignType)

# add upload_file 
from graphene_file_upload.scalars import Upload

# Query

class Customers(graphene.ObjectType):
    customers = graphene.List(CustomerType,id=graphene.ID(),name=graphene.String())
    def resolve_Permissions(self, info, id=None, name=None):
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
    def mutate(cls, root, info, name, email):
        customer = Customer(name=name, email=email)
        customer.save()      
        return InsertCustomer(customer=customer)


class Query(Customers, ):
    pass

class Mutation(graphene.ObjectType):
    insertCustomer = InsertCustomer.Field()


