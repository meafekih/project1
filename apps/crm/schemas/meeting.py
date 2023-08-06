import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import auth_required, email_duplicate
from apps.base.decorators import filter_resolver
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base
from .customer import Customer
from apps.authentication.models import ExtendUser as User


class Meeting(base):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='meetings')
    participants = models.ManyToManyField(User, related_name='meetings_attended')
    def __str__(self):
        return self.title

class MeetingType(DjangoObjectType):
    class Meta:
        model = Meeting
        fields = '__all__'
        interfaces = [relay.Node]# for pagination


class MeetingConnection(relay.Connection):
    class Meta:
        node = MeetingType      



class Meetings(graphene.ObjectType):
    meetings = graphene.List(MeetingType,#id=graphene.ID(),name=graphene.String())
    **{field: graphene.Argument(graphene.String) for field in MeetingType._meta.fields})

    @auth_required
    @filter_resolver(MeetingType)
    def resolve_meetings(self, info, **kwargs):
        return Meeting.objects.all()
