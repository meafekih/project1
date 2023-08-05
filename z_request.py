""" 
"""
import requests

url = 'http://127.0.0.1:8000/api/'
my_headers = {'Authorization' : 'Bearer {eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjkxMjYwMDk4LCJvcmlnSWF0IjoxNjkxMjU5Nzk4fQ._p4Kyf-N3nyPgOCyi0wHLlxG9oZMLf5tLzeWomHcwOk}'}
body = '''
mutation update_account{
  updateAccount(
    firstName: "Fekih"
    lastName : "Mohamed"
    
  ) {
    success,
    errors
  }
}
'''
 
response = requests.post(
      headers=my_headers,
      url=url, 
      json={"query": body}
    )
if response.status_code == 200:
    print("response status code: ", response.status_code)
    print("response : ", response.content)
      

