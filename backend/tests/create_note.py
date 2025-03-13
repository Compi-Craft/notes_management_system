import requests

url = 'http://127.0.0.1:8000/notes/'

from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
data = {'title': 'My Note 1', 'content': 'This is my first note'}

response = requests.post(url, json=data, headers=headers)

print(response.status_code)
print(response.json())  # If the response is JSON
