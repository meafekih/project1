import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import auth_required, email_duplicate
from apps.base.decorators import filter_resolver
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base


class Lead(base):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    description = models.TextField()
    def __str__(self):
        return self.name


class LeadType(DjangoObjectType):
    class Meta:
        model = Lead
        fields = '__all__'
        interfaces = [relay.Node]# for pagination


class LeadConnection(relay.Connection):
    class Meta:
        node = LeadType      



class Leads(graphene.ObjectType):
    leads = graphene.List(LeadType,#id=graphene.ID(),name=graphene.String())
    **{field: graphene.Argument(graphene.String) for field in LeadType._meta.fields})


    @auth_required
    @filter_resolver(LeadType)
    def resolve_leads(self, info, **kwargs):
        return Lead.objects.all()
