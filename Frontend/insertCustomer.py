import requests
import base64

url = 'http://127.0.0.1:8000/api/' 

mutation = '''
mutation insertCustomer(
  $name: String!,
  $email: String!,
  $phone: String,
  $address: String,
  $fileName: String,
  $file: String
) {
  insertCustomer(
    name: $name,
    email: $email,
    phone: $phone,
    address: $address,
    fileName: $fileName,
    file: $file
  ) {
    customer {
      id
      name
      email
      phone
      address
    }
  }
}
'''
file_name ="b.png"

variables = {
    'name': 'John Doee',
    'email': 'johndoee@example.com',
    'phone': '123456789',
    'address': '123 Main St',
    'fileName': file_name
}

with open('Frontend/'+ file_name, 'rb') as image_file:
    image_data = base64.b64encode(image_file.read()).decode('utf-8')
    variables['file'] = image_data

request_payload = {
    'query': mutation,
    'variables': variables,
}

response = requests.post(url, json=request_payload)

if response.status_code == 200:
    data = response.json()
    print(data)
    customer = data['data']['insertCustomer']['customer']
    print(f"Customer ID: {customer['id']}, Name: {customer['name']}")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
