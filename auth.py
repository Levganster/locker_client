import requests

retry = True

def authenticate(username, password, app):
    url = f"http://{app.host}:{app.port}/auth/token"  # URL of your API
    payload = {"username": username, "password": password}

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True, response.json()  # Return True and the token
        elif response.status_code == 500:
            global retry
            if retry:
                print("500 Error, retrying...")
                authenticate(username, password)
                retry = False
        else:
            return False, response.json()  # Return error
    except Exception as e:
        return False, str(e)