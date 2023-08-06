import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import auth_required, email_duplicate
from apps.base.decorators import filter_resolver
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base


class Product(base):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'
        interfaces = [relay.Node]# for pagination


class ProductConnection(relay.Connection):
    class Meta:
        node = ProductType      



class Products(graphene.ObjectType):
    products = graphene.List(ProductType,#id=graphene.ID(),name=graphene.String())
    **{field: graphene.Argument(graphene.String) for field in ProductType._meta.fields})

    @auth_required
    @filter_resolver(ProductType)
    def resolve_products(self, info, **kwargs):
        return Product.objects.all()
