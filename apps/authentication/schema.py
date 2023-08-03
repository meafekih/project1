import graphene
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations


import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import Group, Permission
from apps.authentication.models import ExtendUser as User

class GroupType(DjangoObjectType):
    class Meta:
        model = Group

class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission



class AssignGroupToUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        group_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, user_id, group_id):
        user = User.objects.get(pk=user_id)
        group = Group.objects.get(pk=group_id)
        user.groups.add(group)
        return AssignGroupToUser(success=True)

class AssignPermissionToGroup(graphene.Mutation):
    class Arguments:
        group_id = graphene.Int(required=True)
        permission_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, group_id, permission_id):
        group = Group.objects.get(pk=group_id)
        permission = Permission.objects.get(pk=permission_id)
        group.permissions.add(permission)
        return AssignPermissionToGroup(success=True)



class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    assign_group_to_user = AssignGroupToUser.Field()
    assign_permission_to_group = AssignPermissionToGroup.Field()

 
class Query(UserQuery, MeQuery):
    selectGroups = graphene.List(GroupType)
    selectPermissions = graphene.List(PermissionType)

    def resolve_selectGroups(self, info):
        return Group.objects.all()

    def resolve_selectPermissions(self, info):
        return Permission.objects.all()
     
    
class Mutation(AuthMutation):
    pass


