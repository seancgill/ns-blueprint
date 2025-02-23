import requests
import json
import os
import re
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv(override=True)

# Retrieve the API token
API_TOKEN = os.getenv("API_TOKEN")
print(f"Loaded API_TOKEN: {API_TOKEN}")

def validate_extension(extension):
    """Check if extension is numeric."""
    if not extension.isdigit():
        raise ValueError("Extension must be numeric (e.g., 1001).")
    return extension

def create_device(custID, domain, extension):
    """
    Create a device for a user in the NetSapiens API.
    Args:
        custID (str): Customer ID (e.g., 'sgdemo')
        domain (str): Domain name (e.g., 'sgdemo')
        extension (str): User extension (e.g., '1001')
    """
    url = f"https://{custID}.trynetsapiens.com/ns-api/v2/domains/{domain}/users/{extension}/devices"
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "synchronous": "no",
        "caller-id-number-emergency": "[*]",  # Wildcard as per curl example
        "device-force-notify-new-voicemails-enabled": "no",
        "device-level-call-recording-enabled": "yes",
        "device-push-enabled": "no",
        "device-sip-registration-expiry-seconds": 60,
        "device-sip-registration-ignore-for-presence-calculation": "no",
        "device-sip-registration-ignore-report-enabled": "no",
        "device-sip-no-to-tag-in-cancel": "no",
        "device-srtp-enabled": "no",
        "auto-answer-enabled": "no",
        "recording-configuration": "no",
        "device-sip-nat-traversal-enabled": "automatic",
        "device-provisioning-sip-transport-protocol": "udp",
        "device-provisioning-username": f"{extension}@{custID}",  # Dynamic username
        "device": extension  # Matches the extension as per curl
    }
    
    print(f"Calling API URL: {url}")
    print(f"Request payload: {json.dumps(data, indent=2)}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201, 202]:
        print(f"Device for extension {extension} created successfully")
        print(f"Response: {response.text}")
    else:
        print(f"Failed to create device: {response.status_code}")
        print(response.text)

def create_device_prompt():
    """
    Prompt the user for inputs and create a device.
    """
    while True:
        try:
            custID = input("Enter the customer domain (e.g., sgdemo): ").strip()
            if not custID:
                raise ValueError("Customer domain cannot be empty.")
            domain = input("Enter the domain name (e.g., sgdemo): ").strip()
            if not domain:
                raise ValueError("Domain name cannot be empty.")
            extension = validate_extension(input("Enter the user extension (ID): ").strip())
            break
        except ValueError as e:
            print(f"Error: {e}. Please try again.")
    
    create_device(custID, domain, extension)

if __name__ == "__main__":
    create_device_prompt()