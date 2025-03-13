import requests

url = 'http://127.0.0.1:8000/notes/'

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0MTg3MTcyOH0.M6na-JSfiVUea2Sq1-qYGFnnaPW0oP8Tj3kNT3b5r7Y'

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
data = {'title': 'My Note 2', 'content': 'This is my second note'}

response = requests.post(url, json=data, headers=headers)

print(response.status_code)
print(response.json())  # If the response is JSON
