import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import auth_required, email_duplicate
from apps.base.decorators import filter_resolver
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base
from .customer import Customer


class Contact(base):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    def __str__(self):
        return self.name

class ContactType(DjangoObjectType):
    class Meta:
        model = Contact
        fields = '__all__'
        interfaces = [relay.Node]# for pagination


class ContactConnection(relay.Connection):
    class Meta:
        node = ContactType      



class Contacts(graphene.ObjectType):

    contacts = relay.ConnectionField(ContactConnection, #)
    **{field: graphene.Argument(graphene.String) for field in ContactType._meta.fields})
    


    @auth_required
    @filter_resolver(ContactType)
    def resolve_contacts(self, info, **kwargs):
        return Contact.objects.all()
