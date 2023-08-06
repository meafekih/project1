import graphene
from graphene_django.types import DjangoObjectType
from apps.base.decorators import auth_required, email_duplicate
from apps.base.decorators import filter_resolver
from django.conf import settings
from graphene import relay
from django.db import models
from apps.base.models import base
from .customer import Customer
from apps.authentication.models import ExtendUser as User


class Task(base):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    def __str__(self):
        return self.title


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = '__all__'
        interfaces = [relay.Node]# for pagination


class TaskConnection(relay.Connection):
    class Meta:
        node = TaskType      



class Tasks(graphene.ObjectType):
    tasks = graphene.List(TaskType,#id=graphene.ID(),name=graphene.String())
    **{field: graphene.Argument(graphene.String) for field in TaskType._meta.fields})

    @auth_required
    @filter_resolver(TaskType)
    def resolve_tasks(self, info, **kwargs):
        return Task.objects.all()
