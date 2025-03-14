import requests

# URL of your FastAPI server and the analytics endpoint
url = "http://127.0.0.1:8000/analytics"  # Replace with your actual server URL

# Send a GET request to the /analytics endpoint
response = requests.get(url)

# Check if the response was successful (status code 200)
if response.status_code == 200:
    # Parse and print the JSON response
    analytics_data = response.json()
    print("Analytics Data:")
    print(analytics_data)
else:
    print(f"Error: {response.status_code}, {response.text}")
