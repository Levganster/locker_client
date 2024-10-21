import requests


def authenticate(username, password, host, port):
    url = f"http://{host}:{port}/auth/token"  # URL of your API
    payload = {
        "username": username,
        "password": password
    }

    print(url)
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return True, response.json()  # Return True and the token
    else:
        return False, response.json()  # Return error