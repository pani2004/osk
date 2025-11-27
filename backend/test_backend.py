import requests
import json

# Test data
test_data = {
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Subject",
    "message": "This is a test message from the Python backend."
}

# Send POST request
response = requests.post(
    "http://localhost:8000/api/contact",
    headers={"Content-Type": "application/json"},
    data=json.dumps(test_data)
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")