import requests

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0dXNlciJ9.Lfu5W6lM7CUNgQFJi30Xi0oYCzK9-sC9AnY_5Dq2lV8'

url = 'http://127.0.0.1:8000/notes/1'
headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.delete(url, headers=headers)

print(response.status_code)
print(response.json())  # If the response is JSON
