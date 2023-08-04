from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

@csrf_exempt
def graphql_view(request):
    # This view handles GraphQL requests
    return GraphQLView.as_view(graphiql=True)(request)

def index(request):
    # This view renders the index.html file
    return render(request, 'index.html')

