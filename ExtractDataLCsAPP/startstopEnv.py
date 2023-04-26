import requests

# Adres URL do wykonania zapytania na API autoryzacyjnym Azure AD.
url = 'https://login.microsoftonline.com/TenantID/oauth2/v2.0/token'

# Identyfikator klienta  w Azure AD
client_id = 'CLIENT_ID_FROM_AZURE_CLIENT_APP'

# Zakres zasobów, na które aplikacja kliencka ma uzyskać dostęp.
scope = 'https://lcsapi.lcs.dynamics.com//.default'

# Adres e-mail 
username = 'USER_EMAIL_ADDRESS'

# Hasło użytkownika
password = 'PASSWORD'

# Dane do wysłania
payload = {
    'client_id': client_id,
    'scope': scope,
    'username': username,
    'password': password,
    'grant_type': 'password'
}

# Nagłówki żądania POST.
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
}

# Wysłanie żądania POST i zapisanie odpowiedzi HTTP.
response = requests.post(url, data=payload, headers=headers)


print(response.text)

# Pobranie tokena dostępu z odpowiedzi HTTP.
token = response.json()["access_token"]



# Adres URL do wykonania zapytania POST na API Azure Resource Manager.
url = 'https://management.azure.com/environment/v1/start/project/{projectId}/environment/{environmentId}'

# Identyfikator projektu.
project_id = 'your_project_id'

# Identyfikator środowiska.
environment_id = 'your_environment_id'

# Nagłówki żądania POST.
headers = {
    'Authorization': 'Bearer ' + token,  # Token dostępu jako część nagłówka autoryzacyjnego.
    'x-ms-version': '2017-09-15',
    'Content-Type': 'application/json'
}

# Wysłanie żądania POST i zapisanie odpowiedzi HTTP.
response = requests.post(url.format(projectId=project_id, environmentId=environment_id), headers=headers)

# Wyświetlenie odpowiedzi HTTP w formacie tekstowym.
print(response.text)
