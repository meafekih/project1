import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import auth_required, email_duplicate
from apps.base.decorators import filter_resolver
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base
from .customer import Customer


class Opportunity(base):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='opportunities')  
    def __str__(self):
        return self.name


class OpportunityType(DjangoObjectType):
    class Meta:
        model = Opportunity
        fields = '__all__'
        interfaces = [relay.Node]# for pagination


class OpportunityConnection(relay.Connection):
    class Meta:
        node = OpportunityType      



class opportunitys(graphene.ObjectType):
    Opportunitys = graphene.List(OpportunityType,#id=graphene.ID(),name=graphene.String())
    **{field: graphene.Argument(graphene.String) for field in OpportunityType._meta.fields})

    @auth_required
    @filter_resolver(OpportunityType)
    def resolve_opportunitys(self, info, **kwargs):
        return Opportunity.objects.all()
