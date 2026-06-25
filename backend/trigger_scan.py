import requests
import base64

# 1. Login
login_response = requests.post("http://localhost:5001/api/auth/login", json={
    "email": "audit@test.com",
    "password": "Password123"
})
login_data = login_response.json()
print("Login Status:", login_response.status_code)

token = login_data["access_token"]

# 2. Upload Scan
with open(r"C:\Users\sinha\OneDrive\Desktop\AgroGuard\backend\venv\Lib\site-packages\coverage\htmlfiles\favicon_32.png", "rb") as f:
    files = {"image": ("test_image.png", f, "image/png")}
    data = {"crop": "Tomato"}
    headers = {"Authorization": f"Bearer {token}"}
    
    print("Uploading scan...")
    scan_response = requests.post("http://localhost:5001/api/scans", files=files, data=data, headers=headers)
    print("Scan Response:", scan_response.status_code, scan_response.text)
