import requests
import json

# 1. Login
login_response = requests.post("http://localhost:5001/api/auth/login", json={
    "email": "audit@test.com",
    "password": "Password123"
})
login_data = login_response.json()
token = login_data["access_token"]

# 2. Get History
headers = {"Authorization": f"Bearer {token}"}
history_response = requests.get("http://localhost:5001/api/scans", headers=headers)
print("History Response:", history_response.status_code)
print(json.dumps(history_response.json(), indent=2))
