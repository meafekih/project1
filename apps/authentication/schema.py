import graphene
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations


import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import Group, Permission
from apps.authentication.models import ExtendUser as User
from .decorators import filter_resolver

class GroupType(DjangoObjectType):
    class Meta:
        model = Group

class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission


class Groups(graphene.ObjectType):
    # make all fields of groups as arguments but all fields considere String
    groups = graphene.List(GroupType, #id=graphene.ID(), name=graphene.String())
    **{field: graphene.Argument(graphene.String) for field in GroupType._meta.fields})

    @filter_resolver(GroupType)
    def resolve_groups(self, info, **kwargs):
        return Group.objects.all()

class Permissions(graphene.ObjectType):
    permissions = graphene.List(PermissionType, 
    **{field: graphene.Argument(graphene.String) for field in PermissionType._meta.fields})
    
    @filter_resolver(PermissionType)
    def resolve_permissions(self, info, **kwargs):
        return Permission.objects.all()



class InsertGroup(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        permissions= graphene.List(graphene.Int, required=False)

    group = graphene.Field(GroupType)
    
    @classmethod
    def mutate(cls, root, info, name, permissions):
        group = Group(name=name)
        group.save()
        #associated_model = permission.content_type.model_class()
        #app_label = associated_model._meta.app_label
        #print(associated_model.__name__)
        permission_objs = Permission.objects.filter(id__in=permissions)
        group.permissions.set(permission_objs)
        
        return InsertGroup(group=group)

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
        permissions_id = graphene.List(graphene.Int, required=True)

    success = graphene.Boolean()

    def mutate(self, info, group_id, permissions_id):
        group = Group.objects.get(pk=group_id)
        #permission = Permission.objects.get(pk=permission_id)
        #group.permissions.add(permission)
        permission_objs = Permission.objects.filter(id__in=permissions_id)
        group.permissions.set(permission_objs)

        return AssignPermissionToGroup(success=True)



class AuthMutations(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()

    assign_group_to_user = AssignGroupToUser.Field()
    InsertGroup = InsertGroup.Field()
    assign_permission_to_group = AssignPermissionToGroup.Field()

 
 

class Query(UserQuery, MeQuery, Groups, Permissions):
    pass

class Mutation(AuthMutations):
    pass


