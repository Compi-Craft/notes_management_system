import requests

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc0MTg3MTcyOH0.M6na-JSfiVUea2Sq1-qYGFnnaPW0oP8Tj3kNT3b5r7Y'

url = 'http://127.0.0.1:8000/notes/1'
headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.delete(url, headers=headers)

print(response.status_code)
print(response.json())  # If the response is JSON
