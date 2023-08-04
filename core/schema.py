import graphene
from apps.authentication.schema import Query as authenticationQuery, Mutation as authenticationMutation
from apps.libreary.schema import Query as librearyQuery, Mutation as librearyMutation
from apps.crm.schema import Query as crmQuery, Mutation as crmMutation
# import other app schemas as needed

class Query(
    authenticationQuery,
    librearyQuery, 
    crmQuery,
    graphene.ObjectType):
    pass

class Mutation(
    authenticationMutation,
    librearyMutation,
    crmMutation,
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
