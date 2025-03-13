import requests

url = 'http://127.0.0.1:8000/users/'
headers = {'Content-Type': 'application/json'}
data = {'username': 'testuser', 'password': 'securepassword'}

response = requests.post(url, json=data, headers=headers)

print(response.status_code)
print(response.text)  # If the response is JSON
