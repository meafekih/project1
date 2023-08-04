import graphene
from graphene_django.types import DjangoObjectType
from .models import Product
from graphene_file_upload.scalars import Upload


class ProductType(DjangoObjectType):
    class Meta:
        model = Product



class UploadProductFile(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)
    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        if file:
            with open('media/' + file.name, 'wb',encoding="utf8", ) as f:
                f.read()
        return UploadProductFile(success = True)






class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()
    
class Mutation(graphene.ObjectType):
    uploadProductFile = UploadProductFile.Field()
 














