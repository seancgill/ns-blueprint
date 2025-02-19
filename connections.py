import requests
import json
import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

# Retrieve the API token
API_TOKEN = os.getenv("API_TOKEN")

def get_api_url(domain):

    return f"https://{domain}.trynetsapiens.com/ns-api/v2/connections"

def create_connection(domain):
    """
    Create a connection via the API.
    
    Parameters:
      - domain: the host ID (e.g. 'sgdemo')
      - description: a description for the connection
      - translation_source_host: value for the "connection-translation-source-host"
      
    Returns:
      - The response from the API.
    """
    translation_source_host = f"{domain}.trynetsapiens.com"
    url = get_api_url(domain)
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_TOKEN}",
        "content-type": "application/json"
    }
    # Build the payload matching your curl data
    payload = {
        "connection-orig-enabled": "yes",
        "connection-term-enabled": "yes",
        "connection-translation-destination-host": "192.81.236.20",
        "connection-translation-request-user": "[*]",
        "connection-translation-destination-user": "[*]",
        "connection-translation-source-user": "[*]",
        "connection-source-ip-checking-enabled": "yes",
        "connection-include-server-header-enabled": "no",
        "connection-relay-comfort-noise-enabled": "system-default",
        "connection-pcmu-only-enabled": "no",
        "connection-enforce-minimum-duration-enabled": "no",
        "connection-bind-to-alternate-interface-enabled": "no",
        "connection-block-video-in-sdp-enabled": "no",
        "connection-sip-get-new-dialog-destination-from": "default-ip",
        "connection-sip-get-response-destination-from": "default-ip",
        "connection-require-encrypted-audio-enabled": "no",
        "connection-sip-transport-protocol": "UDP",
        "connection-check-orig-matching-sip-header": "from",
        "connection-sip-session-timer-enabled": "system-default",
        "connection-prevent-rtp-port-change-enabled": "no",
        "connection-hide-post-dial-delay-with-ringback-enabled": "no",
        "connection-remote-ringback-handling": "allowed",
        "connection-block-media-in-sip-180-ringing": "no",
        "connection-allow-mid-call-uri-updates-enabled": "no",
        "connection-record-all-calls-enabled": "no",
        "connection-require-sip-authentication-enabled": "no",
        "minimum-call-duration-seconds": 0,
        "connection-sip-authenticate-as-client-enabled": "no",
        "connection-is-carrier-trunk": "yes",
        "connection-orig-match-pattern": "sip*@192.81.236.20",
        "connection-term-match-pattern": "sip:*@192.81.236.20",
        "domain": "*",
        "description": "ThinQ Secondary Orig & 911",
        "connection-audio-relay-enabled": "yes",
        "connection-address": "192.81.236.20",
        "dial-plan": "Inbound DID",
        "dial-policy": "Permit All",
        "connection-linked-billing-user": "domain",
        "connection-translation-request-host": "192.81.236.20",
        "connection-custom-p-asserted-id-format": "passerted",
        "connection-translation-source-host": translation_source_host,
        "utc-offset": "-7",
        "time-zone": "US/Pacific"
    }
    
    # Log the URL being called for troubleshooting
    print(f"Calling API URL: {url}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error calling {url} with payload {payload}")
        print(f"Exception: {e}")
        raise


def create_second_connection(domain):

    translation_source_host = f"{domain}.trynetsapiens.com"
    url = get_api_url(domain)
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_TOKEN}",
        "content-type": "application/json"
    }
    
    # Build the payload matching your second connection's curl data
    payload = {
        "connection-orig-enabled": "yes",
        "connection-term-enabled": "yes",
        "connection-translation-destination-host": "192.81.237.20",
        "connection-translation-request-user": "[*]",
        "connection-translation-destination-user": "[*]",
        "connection-translation-source-user": "[*]",
        "connection-source-ip-checking-enabled": "yes",
        "connection-include-server-header-enabled": "no",
        "connection-relay-comfort-noise-enabled": "system-default",
        "connection-pcmu-only-enabled": "no",
        "connection-enforce-minimum-duration-enabled": "no",
        "connection-bind-to-alternate-interface-enabled": "no",
        "connection-block-video-in-sdp-enabled": "no",
        "connection-sip-get-new-dialog-destination-from": "default-ip",
        "connection-sip-get-response-destination-from": "default-ip",
        "connection-require-encrypted-audio-enabled": "no",
        "connection-sip-transport-protocol": "UDP",
        "connection-check-orig-matching-sip-header": "from",
        "connection-sip-session-timer-enabled": "system-default",
        "connection-prevent-rtp-port-change-enabled": "no",
        "connection-hide-post-dial-delay-with-ringback-enabled": "no",
        "connection-remote-ringback-handling": "allowed",
        "connection-block-media-in-sip-180-ringing": "no",
        "connection-allow-mid-call-uri-updates-enabled": "no",
        "connection-record-all-calls-enabled": "no",
        "connection-require-sip-authentication-enabled": "no",
        "minimum-call-duration-seconds": 0,
        "connection-sip-authenticate-as-client-enabled": "no",
        "connection-is-carrier-trunk": "yes",
        "connection-orig-match-pattern": "sip*@192.81.237.20",
        "connection-term-match-pattern": "sip:*@192.81.237.20",
        "domain": "*",
        "description": "ThinQ Primary Orig & 911",
        "connection-audio-relay-enabled": "yes",
        "connection-address": "192.81.237.20",
        "dial-plan": "Inbound DID",
        "dial-policy": "Permit All",
        "connection-linked-billing-user": "domain",
        "connection-translation-request-host": "192.81.237.20",
        "connection-custom-p-asserted-id-format": "passerted",
        "connection-translation-source-host": translation_source_host,
        "utc-offset": "-7",
        "time-zone": "US/Pacific"
    }
    
    # Log the API URL being called for troubleshooting
    print(f"Calling API URL: {url}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error calling {url} with payload {payload}")
        print(f"Exception: {e}")
        raise

def create_outbound_connection(domain):
    translation_source_host = f"{domain}.trynetsapiens.com"
    url = get_api_url(domain)
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_TOKEN}",
        "content-type": "application/json"
    }
    
    # Build the payload matching your second connection's curl data
    payload = {
        "connection-orig-enabled": "yes",
        "connection-term-enabled": "yes",
        "connection-translation-destination-host": "a.icr.commio.com",
        "connection-translation-request-user": "[*]",
        "connection-translation-destination-user": "[*]",
        "connection-translation-source-user": "[*]",
        "connection-source-ip-checking-enabled": "yes",
        "connection-include-server-header-enabled": "no",
        "connection-relay-comfort-noise-enabled": "system-default",
        "connection-pcmu-only-enabled": "no",
        "connection-enforce-minimum-duration-enabled": "no",
        "connection-bind-to-alternate-interface-enabled": "no",
        "connection-block-video-in-sdp-enabled": "no",
        "connection-sip-get-new-dialog-destination-from": "default-ip",
        "connection-sip-get-response-destination-from": "default-ip",
        "connection-require-encrypted-audio-enabled": "no",
        "connection-sip-transport-protocol": "UDP",
        "connection-check-orig-matching-sip-header": "from",
        "connection-sip-session-timer-enabled": "system-default",
        "connection-prevent-rtp-port-change-enabled": "no",
        "connection-hide-post-dial-delay-with-ringback-enabled": "no",
        "connection-remote-ringback-handling": "allowed",
        "connection-block-media-in-sip-180-ringing": "no",
        "connection-allow-mid-call-uri-updates-enabled": "no",
        "connection-record-all-calls-enabled": "no",
        "connection-require-sip-authentication-enabled": "no",
        "minimum-call-duration-seconds": 0,
        "connection-sip-authenticate-as-client-enabled": "no",
        "connection-is-carrier-trunk": "yes",
        "connection-orig-match-pattern": "sip*@a.icr.commio.com",
        "connection-term-match-pattern": "sip:*@a.icr.commio.com",
        "domain": "*",
        "description": "ThinQ LCR Outbound",
        "connection-audio-relay-enabled": "yes",
        "connection-address": "a.icr.commio.com",
        "dial-plan": "Inbound DID",
        "dial-policy": "Permit All",
        "connection-linked-billing-user": "domain",
        "connection-translation-request-host": "a.icr.commio.com",
        "connection-custom-p-asserted-id-format": "passerted",
        "connection-translation-source-host": translation_source_host,
        "utc-offset": "-7",
        "time-zone": "US/Pacific"
    }
    
    # Log the API URL being called for troubleshooting
    print(f"Calling API URL: {url}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error calling {url} with payload {payload}")
        print(f"Exception: {e}")
        raise

if __name__ == "__main__":
    # Prompt user for necessary inputs
    domain = input("Enter the host ID (e.g., sgdemo): ").strip()
    description = input("Enter the connection description: ").strip()
    translation_source_host = input("Enter the connection translation source host (<AppIP> or actual IP): ").strip()
    
    response = create_connection(domain, description, translation_source_host)
    if response.status_code in (201, 202):
        print("Connection created successfully")
    else:
        print(f"Failed to create connection: {response.status_code}")
        print(response.text)
