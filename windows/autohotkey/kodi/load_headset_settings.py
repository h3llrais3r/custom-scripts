import json
import urllib
import requests 

# Required header for Kodi JSON-RPC calls, otherwise you'll get a 415 HTTP response code - Unsupported media type
headers = {'content-type': 'application/json'}

# Host name where Kodi is running, leave as localhost if on this PC
# Make sure "Allow control of Kodi via HTTP" is set to ON in Settings -> Services -> Webserver
host = "localhost"

# User/password for "Allow control of Kodi via HTTP"
user = "kodi"
password = "kodi"

# Configured in Settings -> Services -> Webserver -> Port
port = 8090

# Base URL of the json RPC calls
# For GET calls we append a "request" URI parameter
# For POST calls, we add the payload as JSON the the HTTP request body
json_rpc_url = "http://" + user + ":" + password + "@" + host + ":" + str(port) + "/jsonrpc"

# Load the receiver settings
# Set channels (2.0 channels = 1)
payload_channels = {'jsonrpc': '2.0', 'method': 'Settings.SetSettingValue', 'params': {'setting': 'audiooutput.channels', 'value': 1}, 'id': 1}
url_param_channels = urllib.urlencode({'request': json.dumps(payload_channels)})
# response = requests.get(json_rpc_url + '?' + url_param_channels, headers=headers)
response = requests.post(json_rpc_url, data=json.dumps(payload_channels), headers=headers)
# Set passthrough = false
payload_passthrough = {'jsonrpc': '2.0', 'method': 'Settings.SetSettingValue', 'params': {'setting': 'audiooutput.passthrough', 'value': False}, 'id': 1}
url_param_passthrough = urllib.urlencode({'request': json.dumps(payload_passthrough)})
# response = requests.get(json_rpc_url + '?' + url_param_passthrough, headers=headers)
response = requests.post(json_rpc_url, data=json.dumps(payload_passthrough), headers=headers)

# Show notification if loaded
if response.status_code == 200:
    payload_notification = {'jsonrpc': '2.0', 'method': 'GUI.ShowNotification', 'params': {'title': 'Audio change', 'message': 'Switching to headset output'}, 'id': 1}
    url_param_notification = urllib.urlencode({'request': json.dumps(payload_notification)})
    # requests.get(json_rpc_url + '?' + url_param_notification, headers=headers)
    requests.post(json_rpc_url, data=json.dumps(payload_notification), headers=headers)
else:
    print response.status_code
    print response.content
