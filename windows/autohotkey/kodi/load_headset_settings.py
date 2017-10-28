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

#Payload for the method to load the headset settings (2.0 channels = 1)
payload = {'jsonrpc': '2.0', 'method': 'Settings.SetSettingValue', 'params': {'setting': 'audiooutput.channels', 'value': 1}, 'id': 1}
url_param = urllib.urlencode({'request': json.dumps(payload)})

#Load the headset settings
response = requests.get(xbmc_json_rpc_url + '?' + url_param, headers=headers)

#Show notification if loaded
if response.status_code == 200:
    #Payload for the method to show a notification of the change
    payload = {'jsonrpc': '2.0', 'method': 'GUI.ShowNotification', 'params': {'title': 'Audio change', 'message': 'Switching to headset output'}, 'id': 1}
    url_param = urllib.urlencode({'request': json.dumps(payload)})
    requests.get(xbmc_json_rpc_url + '?' + url_param, headers=headers)
else:
    print response.status_code