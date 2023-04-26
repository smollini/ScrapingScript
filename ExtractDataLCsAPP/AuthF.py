import requests
import json
from bs4 import BeautifulSoup


def parse_config_json(response_content):
    """
    Parse the $Config JSON data from the response content.

    Args:
        response_content (bytes): The response content as bytes.

    Returns:
        dict: The parsed JSON data from the $Config variable.
    """
    # Parse the response content as HTML
    soup = BeautifulSoup(response_content, 'html.parser')
    print(response_content)
    # Extract the value from the $Config variable
    config_script = soup.find('script', string=lambda t: t and '$Config' in t)
    if config_script:
        config_data = config_script.string.strip().replace(
            '$Config=', '').replace(';', '')
        json_data = config_data.replace('//<![CDATA[', '').replace('//]]>', '')

        # Parse the data as JSON
        try:
            config_json = json.loads(json_data)
            return config_json
        except json.JSONDecodeError:
            print("Failed to parse $Config as JSON")
            return None
    else:
        print("$Config not found in HTML")
        return None


def create_login_request_body(html, username, password):
    """
    Extracts the necessary parameters from the config JSON object to create the login request body.

    Args:
        html (bytes): The response content from the login page.
        username (str): The username to use for logging in.
        password (str): The password to use for logging in.

    Returns:
        dict: The login request body with the required parameters.
              Returns None if the config JSON is not found or parsing fails.
    """
    config_json = parse_config_json(html)
    if config_json:
        # Extract specific values from the parsed JSON
        sFT = config_json.get("sFT")
        canary = config_json.get("canary")
        sCtx = config_json.get("sCtx")
        sessionId = config_json.get("sessionId")

        # Define the login request body with the required parameters
        body = {
            'i13': 0,
            'login': username,
            'loginfmt': username,
            'type': 11,
            'LoginOptions': 3,
            'lrt': '',
            'lrtPartition': '',
            'hisRegion': '',
            'hisScaleUnit': '',
            'passwd': password,
            'ps': 2,
            'psRNGCDefaultType': '',
            'psRNGCEntropy': '',
            'psRNGCSLK': '',
            'canary': canary,
            'ctx': sCtx,
            'hpgrequestid': sessionId,
            'flowToken': sFT,
            'PPSX': '',
            'NewUser': 1,
            'FoundMSAs': '',
            'fspost': 0,
            'i21': 0,
            'CookieDisclosure': 0,
            'IsFidoSupported': 1,
            'isSignupPost': 0,
            'i19': 575733,
        }
        return body
    else:
        return None


def loginTo(response_content, username, password):
    """
    Logs in to the Microsoft account using the provided credentials.

    Args:
        response_content (bytes): The response content from the login page.
        username (str): The username to use for logging in.
        password (str): The password to use for logging in.

    Returns:
        requests.Response: The login response from the server.
    """
    # Create the request body using the response content
    body = create_login_request_body(response_content, username, password)

    if body:
        # Use the session to send a POST request with the login credentials

        login_response = session.post(
            'https://login.microsoftonline.com/common/login', data=body)
        print('Login response status code:', login_response.status_code)
        return login_response
    else:
        print('Error creating login request body')


def create_response_kmsi(response_content):
    """
    Create the KMSI login response using the response content from the initial login request.

    Args:
        response_content (bytes): The response content from the initial login request.

    Returns:
        requests.Response: The response from the KMSI login request.
    """
    # Create the request body using the response content
    body = create_body_kmsi(response_content)
    if body:
        # Use the session to send a POST request with the login credentials
        kmsi_response = session.post(
            'https://login.microsoftonline.com/kmsi', data=body)
        print('Login kmsi response status code:', kmsi_response.status_code)
        return kmsi_response
    else:
        print('Error creating login request body')


def create_body_kmsi(response_content):
    """
    Create the request body for KMSI login using the response content.

    Args:
    response_content (bytes): The response content from the initial login request.

    Returns:
    dict or None: The request body as a dictionary, or None if the config JSON cannot be parsed.
    """
    config_json = parse_config_json(response_content)
    if config_json:
        # Extract specific values from the parsed JSON
        sFT = config_json.get("sFT")
        canary = config_json.get("canary")
        sCtx = config_json.get("sCtx")
        sessionId = config_json.get("sessionId")

        body = {
            "LoginOptions": 3,
            "type": 28,
            "ctx": sCtx,
            "hpgrequestid": sessionId,
            "flowToken": sFT,
            "canary": canary,
            "i19": 9073
        }
        return body
    else:
        return None


def create_Dynamics_request_body(response_content):

    # Parse the response using BeautifulSoup
    soup = BeautifulSoup(response_content, 'html.parser')

# Get values from hidden input fields
    code = soup.find('input', {'name': 'code'}).get('value')
    id_token = soup.find('input', {'name': 'id_token'}).get('value')
    state = soup.find('input', {'name': 'state'}).get('value')
    session_state = soup.find('input', {'name': 'session_state'}).get('value')

    body = {
        "code": code,
        "id_token": id_token,
        "state": state,
        "session_state": session_state
    }

    return body


def create_Dynamics_response(response_content):
    """
    Create the request body for Dynamics login using the response content.

    Args:
        response_content (bytes): The response content from the initial login request.

    Returns:
        dict: The request body as a dictionary.
    """
    body = create_Dynamics_request_body(response_content)
    url = "https://lcs.dynamics.com/"



    response = session.post(url, headers=headers, data=body)
    return response


def save_headers(response_content):
    """
    Save the response headers and cookies to a JSON file for future use.

    Args:
        response_content (bytes): The response content from the initial login request.

    Returns:
        None.
    """

    with open('odpowiedz4.html', 'wb') as file:
        file.write(response_content)

    soup = BeautifulSoup(response_content, 'html.parser')

    request_verification_token = soup.find(
        'input', {'name': '__RequestVerificationToken'})['value']
    data = {

        "headers": {
            "__RequestVerificationToken": request_verification_token
        },
        "cookies": {
            "lcscs": session.cookies.get("lcscs"),
            "lcsuid": session.cookies.get("lcsuid"),
            "lcsada": session.cookies.get("lcsada"),
            "__RequestVerificationToken": session.cookies.get("__RequestVerificationToken")

        }

    }
    with open('lcs_auth_headers.json', 'w') as f:
        json.dump(data, f)


def start(username, password):
    # Create a session object
    global session
    session = requests.Session()
    # Send a GET request using the session
    response = session.get('https://lcs.dynamics.com/Logon/AdLogon')

    if response.status_code == 200:
        # A response with status code 200 indicates successful access to the resource
        print('Success! Access to resource obtained.')
        # Write the response content to a file
        with open('response.html', 'wb') as file:
            file.write(response.content)
        login_response = loginTo(response.content, username, password)
        if login_response:
            kmsi_response = create_response_kmsi(login_response.content)
            dynamics_response = create_Dynamics_response(kmsi_response.content)
            save_headers(dynamics_response.content)
            session = requests.Session()
            pass
        else:
            print('Error logging in')
    else:
        # A different response code indicates a different scenario, exit the loop
        print('AdLogon returns an invalid status code')
    session.close()



global headers
headers = {
    'Host': 'lcs.dynamics.com',
    'Content-Length': '3031',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://login.microsoftonline.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://login.microsoftonline.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9'
}


