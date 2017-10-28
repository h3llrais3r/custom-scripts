import json
import urllib
import requests 

#Required header for XBMC JSON-RPC calls, otherwise you'll get a 415 HTTP response code - Unsupported media type
headers = {'content-type': 'application/json'}

#Host name where XBMC is running, leave as localhost if on this PC
#Make sure "Allow control of Kodi via HTTP" is set to ON in Settings -> Services -> Webserver
xbmc_host = "localhost"

#User/password for "Allow control of Kodi via HTTP"
user = "kodi"
password = "kodi"

#Configured in Settings -> Services -> Webserver -> Port
xbmc_port = 8090

#Base URL of the json RPC calls. For GET calls we append a "request" URI 
#parameter. For POSTs, we add the payload as JSON the the HTTP request body
xbmc_json_rpc_url = "http://" + user + ":" + password + "@" + xbmc_host + ":" + str(xbmc_port) + "/jsonrpc"

#Load the receiver settings
#Set channels (5.1 channels = 8)
payload_channels = {'jsonrpc': '2.0', 'method': 'Settings.SetSettingValue', 'params': {'setting': 'audiooutput.channels', 'value': 8}, 'id': 1}
url_param_channels = urllib.urlencode({'request': json.dumps(payload_channels)})
response = requests.get(xbmc_json_rpc_url + '?' + url_param_channels, headers=headers)
#Set passthrough = true
payload_passthrough = {'jsonrpc': '2.0', 'method': 'Settings.SetSettingValue', 'params': {'setting': 'audiooutput.passthrough', 'value': true}, 'id': 1}
url_param_passthrough = urllib.urlencode({'request': json.dumps(payload_passthrough)})
response = requests.get(xbmc_json_rpc_url + '?' + url_param, headers=headers)

#Show notification if loaded
if response.status_code == 200:
    payload_notification = {'jsonrpc': '2.0', 'method': 'GUI.ShowNotification', 'params': {'title': 'Audio change', 'message': 'Switching to receiver output'}, 'id': 1}
    url_param_notification = urllib.urlencode({'request': json.dumps(payload_notification)})
    requests.get(xbmc_json_rpc_url + '?' + url_param_notification, headers=headers)
else:
    print response.status_code