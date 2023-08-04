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


class selectGroups(graphene.ObjectType):
    Groups = graphene.List(GroupType, 
    **{field_name: graphene.Argument(graphene.String) for field_name in GroupType._meta.fields})
    def resolve_Groups(self, info, **kwargs):
        queryset = Group.objects.all()
        for n, v in kwargs.items():
            if n in GroupType._meta.fields:
                filter_args = {n: v}
                queryset = queryset.filter(**filter_args)
        return queryset
    
class selectPermissions(graphene.ObjectType):
    Permissions = graphene.List(PermissionType, 
                                id=graphene.ID(),
                                name=graphene.String())
    def resolve_Permissions(self, info, id=None, name=None):
        queryset = Permission.objects.all()
        if id:
            queryset = queryset.filter(id=id)
        if name:
            queryset = queryset.filter(name=name)
        return queryset


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



class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    assign_group_to_user = AssignGroupToUser.Field()
    InsertGroup = InsertGroup.Field()
    assign_permission_to_group = AssignPermissionToGroup.Field()

 
 

class Query(UserQuery, MeQuery, selectGroups, selectPermissions):
    pass



class Mutation(AuthMutation):
    pass


