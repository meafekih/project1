import graphene
from apps.authentication.schema import Query as authenticationQuery, Mutation as authenticationMutation
from apps.libreary.schema import Query as librearyQuery, Mutation as librearyMutation
from apps.quiz.schema import Query as quizQuery, Mutation as quizMutation
from apps.products.schema import Query as productsQuery, Mutation as productsMutation
# import other app schemas as needed

class Query(
    authenticationQuery,
    librearyQuery, 
    quizQuery,
    productsQuery,
    graphene.ObjectType):
    pass

class Mutation(
    authenticationMutation,
    librearyMutation,
    quizMutation,
    productsMutation,
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
