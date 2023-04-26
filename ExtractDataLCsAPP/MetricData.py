import requests
import json
import sys
import time
from datetime import datetime



# Define function to log messages with a timestamp
def log(msg):
   now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   print(f"{now} | {msg}")

# Load authentication headers from file
def get_auth_headers(filename):
    with open(filename, 'r') as json_file:
        return json.load(json_file)

# Write data to file in JSON format
def write_to_file(filename, data):
   try:
      with open(filename, "w+") as f:
          json.dump(data, f)
          log(f"Data written to {filename}")
   except IOError as e:
      log(f"Error writing data to {filename}: {e}")
      sys.exit(1)

# Define function to format the data into a list of dictionaries
def format_data(json_data,customerName):
    formatted_data = []
    for metricName, aosData in json_data.items():
        for aos, metricData in aosData.items():
            for datapoint in metricData["Data"]:
                date = datetime.fromtimestamp(int(datapoint["Date"][6:-2]) / 1000).isoformat()
                value = datapoint["Value"]
                formatted_data.append({"Date": date, "Value": value,"AOS": aos, "MetricName": metricName,"customer": customerName})

     #result = {}
    #for item in formatted_data:
    ##    aos = item["AOS"]
     #   result.setdefault(aos, [])
     #   result[aos].append(item)
    write_to_file('mem',formatted_data)
    return formatted_data




def get_MemAvalible_data(envId, projId,customerName):
    """
    Get metric data from Dynamics for a given environment and project.

    Args:
        envId (str): The ID of the environment to retrieve metric data from.
        projId (str): The ID of the project associated with the environment.
        startTime (str): The start time for the metric data range in format "yyyy-MM-ddTHH:mm:ssZ".
        endTime (str): The end time for the metric data range in format "yyyy-MM-ddTHH:mm:ssZ".

    Returns:
        dict: A dictionary containing the formatted metric data.
    """
    current_time = int(time.time()) * 1000
    start = current_time - (60 * 60 * 1000)
    end = current_time
    # Load the authentication headers from file
    auth_headers = get_auth_headers('lcs_auth_headers.json')
    headers = auth_headers['headers']
    headers.update({'accept': '*/*',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest'})
    cookies = auth_headers['cookies']

    # Make the request to get the data
    url = f'https://diag.lcs.dynamics.com/ComponentMonitors/GetMetricData/{projId}?environmentId={envId}'
    data = {'startStr': start,
            'endStr': end,
            'maxPntsStr': 200,
            'metrics[]': '\\Memory\\Available MBytes',
            'serviceUnit': 'westeurope.thisisidaswell'}
    try:
        response = requests.post(url, data=data, headers=headers, cookies=cookies, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        log(f"Error retrieving data: {e}")
        sys.exit(1)

    # Format the response data and return it
    formatted_data = format_data(response.json(),customerName)
    return formatted_data

def get_Cpu_data(envId, projId,customerName):
    """
    Get metric data from Dynamics for a given environment and project.

    Args:
        envId (str): The ID of the environment to retrieve metric data from.
        projId (str): The ID of the project associated with the environment.
        customerName(str)define which customer logs

    Returns:
        dict: A dictionary containing the formatted metric data.
    """
    current_time = int(time.time()) * 1000
    start = current_time - (60 * 60 * 1000)
    end = current_time
    # Load the authentication headers from file
    auth_headers = get_auth_headers('lcs_auth_headers.json')
    headers = auth_headers['headers']
    headers.update({'accept': '*/*',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest'})
    cookies = auth_headers['cookies']

    # Make the request to get the data
    url = f'https://diag.lcs.dynamics.com/ComponentMonitors/GetMetricData/{projId}?environmentId={envId}'
    data = {'startStr': start,
            'endStr': end,
            'maxPntsStr': 200,
            'metrics[]': '\\Processor(_Total)\\% Processor Time',
            'serviceUnit': 'westeurope.thisisidaswell'}
    try:
        response = requests.post(url, data=data, headers=headers, cookies=cookies, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        log(f"Error retrieving data: {e}")
        sys.exit(1)

    # Format the response data and return it
    formatted_data = format_data(response.json(),customerName)
    return formatted_data



