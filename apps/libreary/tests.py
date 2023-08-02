""" 
from django.test import TestCase

# my_app/tests.py
import json
from graphene_django.utils.testing import GraphQLTestCase
from .models import Author

class AuthorGraphQLTestCase(GraphQLTestCase):
    # Load the GraphQL schema from your main schema.py
    #GRAPHQL_SCHEMA = 'project_name.schema.schema'

    def setUp(self):
        # Create some test data for Author
        Author.objects.create(name='author 1', email='author1@email.com', bio='biblio for author 1')
        Author.objects.create(name='author 2', email='author2@email.com', bio='biblio for author 2')

    def test_query(self):
        response = self.query(
            '''
            query {Author(id: 1) {id name email bio}}
            '''
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['Author']['name'], 'author 1')

    def test_mutation(self):
        response = self.query(
            '''
            mutation {InsertAuthor(input: {name: "author 3", email: "author3@email.com", bio: "bio of author 3"}) 
            {Author { id name email }}}
            '''
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['createAuthor']['Author']['name'], 'author 3')

 """

import json
import pytest
from graphene_django.utils.testing import graphql_query

@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)
    return func

# Test you query using the client_query fixture
def test_some_query(client_query):
    response = client_query(
        '''
        query {Author(id: 1) {id name email bio}}
        ''',
        op_name='Author'
    )

    content = json.loads(response.content)
    assert 'errors' not in content