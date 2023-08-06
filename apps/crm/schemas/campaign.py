import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import auth_required, email_duplicate
from apps.base.decorators import filter_resolver
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base
from .lead import Lead


class Campaign(base):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    leads = models.ManyToManyField(Lead, related_name='campaigns')
    def __str__(self):
        return self.name

class CampaignType(DjangoObjectType):
    class Meta:
        model = Campaign
        fields = '__all__'
        interfaces = [relay.Node]# for pagination


class CampaignConnection(relay.Connection):
    class Meta:
        node = CampaignType      



class Campaigns(graphene.ObjectType):
    campaigns = graphene.List(CampaignType,#id=graphene.ID(),name=graphene.String())
    **{field: graphene.Argument(graphene.String) for field in CampaignType._meta.fields})

    @auth_required
    @filter_resolver(CampaignType)
    def resolve_campaigns(self, info, **kwargs):
        return Campaign.objects.all()
