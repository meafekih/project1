import graphene
from apps.authentication.schema import Query as authenticationQuery, Mutation as authenticationMutation
from apps.crm.schema import Query as crmQuery, Mutation as crmMutation, subscription as crmSubscription

# import other app schemas as needed

class Query(
    authenticationQuery,
    crmQuery,
    graphene.ObjectType):
    pass

class Mutation(
    authenticationMutation,
    crmMutation,
    graphene.ObjectType):
    pass

class Subscription(
    crmSubscription,
    graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
