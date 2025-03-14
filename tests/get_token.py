import requests

url = 'http://127.0.0.1:8000/token'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {'username': 'testuser', 'password': 'securepassword'}

response = requests.post(url, data=data, headers=headers)

print(response.status_code)
print(response.json())  # If the response is JSON
