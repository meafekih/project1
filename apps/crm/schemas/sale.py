import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import auth_required, email_duplicate
from apps.base.decorators import filter_resolver
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base
from .customer import Customer
from .product import Product


class Sale(base):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales')
    products = models.ManyToManyField(Product, related_name='sales')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()
    def __str__(self):
        return f"Sale for {self.customer} on {self.sale_date}"


class SaleType(DjangoObjectType):
    class Meta:
        model = Sale
        fields = '__all__'
        interfaces = [relay.Node]# for pagination


class SaleConnection(relay.Connection):
    class Meta:
        node = SaleType      



class Sales(graphene.ObjectType):
    sales = graphene.List(SaleType,#id=graphene.ID(),name=graphene.String())
    **{field: graphene.Argument(graphene.String) for field in SaleType._meta.fields})

    @auth_required
    @filter_resolver(SaleType)
    def resolve_sales(self, info, **kwargs):
        return Sale.objects.all()
