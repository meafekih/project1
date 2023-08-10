import requests
upload_url = "http://127.0.0.1:8000/upload/"
file_path = "test.txt"
files = {'file': open(file_path, 'rb')}
response = requests.post(upload_url, files=files)

print(response.status_code)
print(response.text)
