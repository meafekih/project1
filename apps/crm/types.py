import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import (Customer, Contact, Opportunity, Task,
                    Product, Sale, Meeting, Lead, Campaign)
from graphene import relay

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'

class ContactType(DjangoObjectType):
    class Meta:
        model = Contact
        fields = '__all__'

class OpportunityType(DjangoObjectType):
    class Meta:
        model = Opportunity
        fields = '__all__'

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = '__all__'

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'
        interfaces = [relay.Node]# for pagination

class SaleType(DjangoObjectType):
    class Meta:
        model = Sale
        fields = '__all__'

class MeetingType(DjangoObjectType):
    class Meta:
        model = Meeting
        fields = '__all__'

class LeadType(DjangoObjectType):
    class Meta:
        model = Lead
        fields = '__all__'

class CampaignType(DjangoObjectType):
    class Meta:
        model = Campaign
        fields = '__all__'


class ProductConnection(relay.Connection):
    class Meta:
        node = ProductType
