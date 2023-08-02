import graphene
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()

 
class Query(UserQuery, MeQuery):
    pass
     
    
class Mutation(AuthMutation):
    pass



