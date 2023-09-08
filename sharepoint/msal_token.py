# pylint: skip-file

from msal import ConfidentialClientApplication
import requests


TENANT_ID = 'tenant-id'
CLIENT_ID = 'client-id'
CLIENT_SECRET = "client-secret"
SCOPE = 'https://bosch.sharepoint.com/.default'


app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
)

result = app.acquire_token_silent([SCOPE], account=None)

if not result:
    result = app.acquire_token_for_client(scopes=[SCOPE])
    print(result)

token = result["access_token"]

headers = {'Authorization': f'Bearer {token}'}

site_api_final = f"https://bosch.sharepoint.com/sites/msteams_6298865/_api/web/GetFolderByServerRelativeUrl('/sites/msteams_6298865/Shared Documents/Neutrinos/')"
request = requests.request("GET", site_api_final, headers=headers).json()
print(request)
