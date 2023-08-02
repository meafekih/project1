import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Author, Category, Publisher, Book, BookInstance

# Types

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = '__all__'

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'

class PublisherType(DjangoObjectType):
    class Meta:
        model = Publisher
        fields = '__all__'

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = '__all__'

class BookInstanceType(DjangoObjectType):
    class Meta:
        model = BookInstance
        fields = '__all__'


# Query

from django.conf import settings

class SelectPublisher(graphene.ObjectType):
    selectPublisher = graphene.List(PublisherType)

    def resolve_selectPublisher(root, info):
        print(settings.LIMIT_CHARS)
        return Publisher.objects.all()
    
class SelectBookInstance(graphene.ObjectType):
    selectBookInstance = graphene.Field(BookInstanceType, id=graphene.Int())

    def resolve_selectBookInstance(root, info, id):
        print(info.context.user)
        return BookInstance.objects.get(pk=id)


# Mutation

class InsertAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email= graphene.String()
        bio = graphene.String()
    
    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, name, email, bio):
        same_email = Author.objects.filter(email=email)
        if same_email:
            print('Email exist !')
            return None
        author = Author(name=name, email=email, bio=bio)
        author.save()
        return InsertAuthor(author=author)
    
class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name=graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return UpdateCategory(category=category)

class DeletePublisher(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    publisher = graphene.Field(PublisherType)

    @classmethod
    def mutate(cls, root, info, id):
        publisher = Publisher.objects.get(id=id)
        publisher.delete()
        return




class Query(SelectBookInstance, SelectPublisher):
    pass

class Mutation(graphene.ObjectType):
    insertAuthor = InsertAuthor.Field()
    updateCategory = UpdateCategory.Field()
    deletePublisher = DeletePublisher.Field()

