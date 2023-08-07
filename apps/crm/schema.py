import graphene

from .schemas.campaign import Campaigns
from .schemas.contact import Contacts
from .schemas.product import Products
from .schemas.customer import (Customers, 
    InsertCustomer, UpdateCustomer, DeleteCustomer)

class Query(Customers, Products, Contacts, Campaigns ):
    pass

class Mutation(graphene.ObjectType):
    insertCustomer = InsertCustomer.Field()
    updateCustomer = UpdateCustomer.Field()
    deleteCustomer = DeleteCustomer.Field()


