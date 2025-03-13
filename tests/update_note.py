import requests

url = 'http://127.0.0.1:8000/notes/1'

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0dXNlciJ9.Lfu5W6lM7CUNgQFJi30Xi0oYCzK9-sC9AnY_5Dq2lV8'

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
data = {'title': 'Updated Title 2', 'content': 'Updated content 2'}

response = requests.put(url, json=data, headers=headers)

print(response.status_code)
print(response.json())  # If the response is JSON
