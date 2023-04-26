import requests
import json

subscription_id = "<Subscription ID>"
resource_group = "<Resource Group Name>"
workspace_name = "<Workspace Name>"
table_name = "<Table Name>"
api_version = "2021-12-01-preview"

url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{resource_group}/providers/Microsoft.OperationalInsights/workspaces/{workspace_name}/tables/{table_name}?api-version={api_version}"


headers = {"Authorization": "Bearer <Access Token>"}


response = requests.get(url, headers=headers)


if response.status_code == 200:
    
    print(json.dumps(response.json(), indent=4))
else:
    
    print(f"Request failed with status code {response.status_code}: {response.text}")