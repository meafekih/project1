from django.contrib import admin
from django.urls import path, include
from apps.crm.views import index
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('api/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)), name='api'),
    
    # if using rest api or views 
    #path('authentication/', include('apps.authentication.urls')),
    #path('libreary/', include('apps.libreary.urls')),
    #path('quiz/', include('apps.quiz.urls')),
    #path('products/', include('apps.products.urls')),
    

]