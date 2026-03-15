import requests

BASE_URL = "https://127.0.0.1:5000"

def main():
    # Normal test data for registration and login.
    register_payload = {"username": "alice", "password": "StrongPass123"}
    login_payload = {"username": "alice", "password": "StrongPass123"}
    # This payload looks like SQL injection and should fail.
    injection_payload = {"username": "' OR 1=1 --", "password": "anything"}

    r1 = requests.post(f"{BASE_URL}/register", json=register_payload, verify=False)
    print("REGISTER:", r1.status_code, r1.text)

    r2 = requests.post(f"{BASE_URL}/login", json=login_payload, verify=False)
    print("LOGIN:", r2.status_code, r2.text)

    r3 = requests.post(f"{BASE_URL}/login", json=injection_payload, verify=False)
    print("SQL INJECTION ATTEMPT:", r3.status_code, r3.text)

if __name__ == "__main__":
    # Hide warnings because this demo uses a local self-signed certificate.
    requests.packages.urllib3.disable_warnings()
    main()
