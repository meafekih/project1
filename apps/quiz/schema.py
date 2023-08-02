import graphene
from graphene_django import DjangoObjectType
from .models import Quiz, Question, Answer, Category

class categoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'

class quizType(DjangoObjectType):
    class Meta:
        model = Quiz
        fields = '__all__'

class questionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = '__all__'

class answerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = '__all__'


class Query(graphene.ObjectType):
    allquizzes = graphene.List(quizType)

    def resolve_allquizzes(root, info):
        return Quiz.objects.all()


class Mutation(graphene.ObjectType):
    pass


