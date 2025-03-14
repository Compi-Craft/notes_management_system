import requests

from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")

url = 'http://127.0.0.1:8000/notes/1'
headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())  # If the response is JSON
