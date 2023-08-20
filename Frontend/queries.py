import random
value = random.randint(0,1000)

def write_response(json_data, query_name):
    posts = json_data['data'][query_name]
    if posts :        
        for key, response_data in posts.items():
            if response_data:  # Skip empty responses
                print(key)
                print(response_data)
                for key2, response_data2 in response_data.items():
                  print(key2 +":"+ response_data2)
    else:
        [error] = json_data['errors']
        print(error['message'])






insertCustomer = '''
mutation insertCustomer($name: String!, $email: String!, $address: String!, $phone: String!){
  insertCustomer(name:$name, email:$email, address:$address, phone:$phone){
    customer{id name address}
  }
}
'''
insertvariables = {
    'name': str(value),
    'email': str(value)+'@email.com',
    'address': str(value)+'@',
    'phone': str(value),
}
 
customers = '''
query Customers{customers{edges{node{ id name email }}}}
'''
customers_variables = {}



deleteCustomer = '''
mutation deleteCustomer{deleteCustomer(email:"455@email.com"){ success }}
'''
deleteCustomer_variables = {}




















