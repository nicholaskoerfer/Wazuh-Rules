#!/usr/bin/python3

import argparse
import json
import urllib.request
import urllib.parse
import sys
import logging
from datetime import datetime, timedelta
from socket import socket, AF_UNIX, SOCK_DGRAM

tenantId = '' # Paste your own tenant ID here
appId = '' # Paste your own app ID here
appSecret = '' # Paste your own app secret here

# Wazuh manager analisysd socket address
socketAddr = '/var/ossec/queue/sockets/queue'

parser = argparse.ArgumentParser(description='SOCFortress Wazuh - Office Defender Non Alerts information.')
args = parser.parse_args()

# Send event to Wazuh manager
def send_event(msg):
    logging.debug('Sending {} to {} socket.'.format(msg, socketAddr))
    string = '1:office_defender:{}'.format(msg)
    sock = socket(AF_UNIX, SOCK_DGRAM)
    sock.connect(socketAddr)
    sock.send(string.encode())
    sock.close()

# Request Token
url = "https://login.microsoftonline.com/%s/oauth2/token" % (tenantId)

resourceAppIdUri = 'https://api.securitycenter.microsoft.com'

body = {
    'resource' : resourceAppIdUri,
    'client_id' : appId,
    'client_secret' : appSecret,
    'grant_type' : 'client_credentials'
}

data = urllib.parse.urlencode(body).encode("utf-8")

# Read Access Token
req = urllib.request.Request(url, data)
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
aadToken = jsonResponse["access_token"]


#build get-alerts API
filterTime = datetime.now() - timedelta(hours = 1)          #If you want to include alerts from longer then an hour, change here (days, weeks)
filterTime = filterTime.strftime("%Y-%m-%dT%H:%M:%SZ")

## Get Machines ##############################################################
url = "https://api.securitycenter.microsoft.com/api/machines"
headers = {
    'Content-Type' : 'application/json',
    'Accept' : 'application/json',
    'Authorization' : "Bearer " + aadToken
}


req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
for alert in jsonResponse["value"]:
        office_defender_event = {}
        office_defender_event['office_defender'] = alert
        office_defender_event['query'] = 'machines'
        send_event(json.dumps(office_defender_event))

## Get Domain Alerts ##############################################################
url = "https://api.securitycenter.microsoft.us/api/domains/*yourdomain*/alerts"
headers = {
    'Content-Type' : 'application/json',
    'Accept' : 'application/json',
    'Authorization' : "Bearer " + aadToken
}


req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
for alert in jsonResponse["value"]:
        office_defender_event = {}
        office_defender_event['office_defender'] = alert
        office_defender_event['query'] = 'domain'
        send_event(json.dumps(office_defender_event))

## Get Recommendations ##############################################################
url = "https://api.securitycenter.microsoft.us/api/recommendations"
headers = {
    'Content-Type' : 'application/json',
    'Accept' : 'application/json',
    'Authorization' : "Bearer " + aadToken
}


req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
for alert in jsonResponse["value"]:
        office_defender_event = {}
        office_defender_event['office_defender'] = alert
        office_defender_event['query'] = 'recommendations'
        send_event(json.dumps(office_defender_event))

## Get Exposure Score  ##############################################################
url = "https://api.securitycenter.microsoft.us/api/exposureScore/ByMachineGroups"
headers = {
    'Content-Type' : 'application/json',
    'Accept' : 'application/json',
    'Authorization' : "Bearer " + aadToken
}


req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
for alert in jsonResponse["value"]:
        office_defender_event = {}
        office_defender_event['office_defender'] = alert
        office_defender_event['query'] = 'exposurescore'
        send_event(json.dumps(office_defender_event))

## Get Software  ##############################################################
url = "https://api.securitycenter.microsoft.us/api/Software"
headers = {
    'Content-Type' : 'application/json',
    'Accept' : 'application/json',
    'Authorization' : "Bearer " + aadToken
}


req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
for alert in jsonResponse["value"]:
        office_defender_event = {}
        office_defender_event['office_defender'] = alert
        office_defender_event['query'] = 'software'
        send_event(json.dumps(office_defender_event))

## Get Vulnerabilities  ##############################################################
url = "https://api.securitycenter.microsoft.us/api/vulnerabilities/machinesVulnerabilities"
headers = {
    'Content-Type' : 'application/json',
    'Accept' : 'application/json',
    'Authorization' : "Bearer " + aadToken
}


req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
for alert in jsonResponse["value"]:
        office_defender_event = {}
        office_defender_event['office_defender'] = alert
        office_defender_event['query'] = 'vulnerabilities'
        send_event(json.dumps(office_defender_event))
