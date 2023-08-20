import requests
import base64

# Read binary image data from a file
with open('media/m.jpeg', 'rb') as image_file:
    binary_data = image_file.read()

# Encode the binary data as base64
base64_encoded_data = base64.b64encode(binary_data).decode('utf-8')

# GraphQL endpoint URL
graphql_url = 'http://127.0.0.1:8000/api/'


# GraphQL mutation query
mutation_query = """

mutation updateCustomer($parameter: String!, $value: String!, $email: String!, $address: String!, $fileName: String!, $file: String!){
  updateCustomer(parameter: $parameter, value: $value ,  email: $email, address: $address,  fileName: $fileName, file: $file){
     customer{
      id
      name
    }
  }
}

"""

# Variables for the mutation
variables = {
    'parameter': 'name',
    'value': 'abc',
    'email': 'abcdef@email.com',
    'address': 'abcdef adress',
    'fileName': 'mm',
    'file': base64_encoded_data
}

# Send the GraphQL request
response = requests.post(graphql_url, json={'query': mutation_query})

# Print the response
print(response.json())



import asyncio
from core.schema import schema

async def main(schema):
    subscription = 'subscription { showTime }'
    result = await schema.subscribe(subscription)
    async for item in result:
        print(item.data['showTime'])

asyncio.run(main(schema))