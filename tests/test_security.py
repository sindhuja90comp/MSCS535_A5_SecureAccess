import requests

BASE_URL = "https://127.0.0.1:5000"

def run_security_check():
    requests.packages.urllib3.disable_warnings()

    payload = {"username": "' OR 1=1 --", "password": "anything"}
    response = requests.post(f"{BASE_URL}/login", json=payload, verify=False)

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    if response.status_code == 401:
        print("PASS: SQL injection attempt failed as expected.")
    else:
        print("FAIL: Unexpected authentication behavior.")

if __name__ == "__main__":
    run_security_check()
