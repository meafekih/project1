import requests
import json
from queries import (write_response,
insertCustomer, insertvariables, customers, customers_variables ,
deleteCustomer, deleteCustomer_variables)

url = 'http://127.0.0.1:8000/api/'
auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjkxMjY2NTc0LCJvcmlnSWF0IjoxNjkxMjY2Mjc0fQ.61IxdjIna7fuA64HydlhCpx4p8OjeiPP_n9W8APMUsY'
headers = {
    'Content-Type': 'application/json',
    #'Authorization': f'Bearer {auth_token}'  
  }
response = requests.post(headers=headers,url=url,json={"query": customers, 'variables': customers_variables})



if response.status_code == 200:
    print("response status code: ", response.status_code)
    #print("response : ", response.content)       
    json_data = response.json()
    print(json_data)
    # Process the JSON response as needed
    #write_response(json_data, 'deleteCustomer')
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)





""""""



