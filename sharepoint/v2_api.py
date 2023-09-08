# pylint: skip-file

import requests

TENANT_ID = 'tenant-id'
CLIENT_ID = 'client-id'
CLIENT_SECRET = "client-secret"
REDIRECT_URI = 'https://bosch.sharepoint.com/auth/callback'
SCOPE = 'https://bosch.sharepoint.com/.default'


def get_code():
    token_api = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize?'
    payload = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": SCOPE, 
        "redirect_uri": REDIRECT_URI, 
        "response_mode":"query",
        "state":12345,
}
    response_token = requests.request("GET", token_api, data=payload, verify=True).content
    print(response_token)
    token = response_token['access_token']

    print(token)
    return token


def get_refresh_token():
    token_api = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": "https://bosch.sharepoint.com/.default",  
    "code": get_code(),
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
    }
    token_response = requests.request("POST", token_api, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
    refresh_token = token_response["refresh_token"] 
    return refresh_token


def get_auth_token():
    token_api = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "refresh_token": get_refresh_token(),
    "scope": f"https://bosch.sharepoint.com/.Sites.Selected",
    "grant_type": "refresh_token",
    }
    token_response = requests.request("POST", token_api, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
    auth_token = token_response["access_token"] 
    headers = {'Authorization': f'Bearer {auth_token}'}
    return headers


def get_auth_token_simple():
    token_api = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": SCOPE,
    "grant_type": "client_credentials",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_response = requests.request("POST", token_api, data=payload, headers=headers).json()
    print(token_response)
    auth_token = token_response["access_token"] 
    headers = {'Authorization': f'Bearer {auth_token}'}
    return headers

def fetch_sharepoint_data():
    site_api_final = f"https://bosch.sharepoint.com/sites/msteams_6298865/_api/web/GetFolderByServerRelativeUrl('/sites/msteams_6298865/Shared Documents/Neutrinos/')"
    request = requests.request("GET", site_api_final, headers=get_auth_token_simple()).json()
    print(request)


if __name__ == "__main__":
    fetch_sharepoint_data()
    