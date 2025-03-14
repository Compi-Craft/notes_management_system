import requests

url = 'http://127.0.0.1:8000/notes/1'

from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
data = {'title': 'Updated Title 2', 'content': 'Updated content 2'}

response = requests.put(url, json=data, headers=headers)

print(response.status_code)
print(response.json())  # If the response is JSON
