# pylint: skip-file

import requests 
from requests.exceptions import HTTPError

TENANT_ID = 'tenant-id'
CLIENT_ID = 'client-id'
CLIENT_SECRET = "client-secret"
RESOURCE = 'https://graph.microsoft.com/'
GRANT_TYPE ='client_credentials'


HOST = 'bosch.sharepoint.com'
SITE_NAME = 'msteams_6298865'
FILE = 'deployment.yaml'


SCOPE = 'https://bosch.sharepoint.com/.default'
REDIRECT_URI = 'https://bosch.sharepoint.com/auth/callback'


def get_site_url(headers):
    response = requests.get(f"https://graph.microsoft.com/v1.0/sites/{HOST}:/sites/{SITE_NAME}", headers=headers).json()
    response_id = response["id"].split(",")
    site_id = response_id[1]
    #print(site_id)  # 19938a33-5c02-4a58-b662-97bab4abcc20 --> https://bosch.sharepoint.com/sites/msteams_6298865/_api/site/id
    return site_id  


def fetch_sharepoint_data():
    try:
        token_api = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"
        payload = f'grant_type={GRANT_TYPE}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&resource={RESOURCE}'
        response_token = requests.request("POST", token_api, data=payload, verify=True).json()
        token = response_token['access_token']
        headers = {'Authorization': f'Bearer {token}'}
  
        SITE_ID = get_site_url(headers)

        site_api = f"https://graph.microsoft.com/v1.0/sites/{HOST},{SITE_ID}/drive/root:/{FILE}"
        response_site = requests.request("GET", site_api, headers=headers, verify=True).json()
        download_url = response_site['@microsoft.graph.downloadUrl']

        download_file = requests.get(download_url)  
        with open('deployment.yaml', 'wb') as output:
            output.write(download_file.content) 
        
        try:
            with open("deployment.yaml", "r") as file:
                file.read()
        except FileNotFoundError:
            print("File not found.")
    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except Exception as err:
        print(f'Erorr occured: {err}')


if __name__ == "__main__":
    fetch_sharepoint_data()
