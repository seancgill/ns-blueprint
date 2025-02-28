import requests
import json
import os
import re
import random
import string
from dotenv import load_dotenv
from logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# Load variables from the .env file into the environment
load_dotenv(override=True)

# Retrieve the API token
API_TOKEN = os.getenv("API_TOKEN")
print(f"Loaded API_TOKEN: {API_TOKEN}")  # Keep for terminal
logger.info(f"Loaded API_TOKEN: {API_TOKEN}")

def generate_random_password(length=12):
    """Generate a random password of specified length using letters, digits, and punctuation."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    logger.info(f"Generated random SIP password of length {length}")
    return password

def validate_extension(extension):
    """Check if extension is numeric."""
    if not extension.isdigit():
        raise ValueError("Extension must be numeric (e.g., 1001).")
    logger.info(f"Validated extension: {extension}")
    return extension

def create_device(custID, domain, extension):
    """
    Create a device for a user in the NetSapiens API with a random 12-character password.
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
    # Generate a random 12-character password
    sip_password = generate_random_password()
    data = {
        "synchronous": "no",
        "caller-id-number-emergency": "[*]",
        "device-force-notify-new-voicemails-enabled": "no",
        "device-level-call-recording-enabled": "no",
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
        "device-sip-registration-password": sip_password,  # Use generated password
        "device": extension
    }
    
    print(f"Calling API URL: {url}")  # Keep for terminal
    logger.info(f"Calling API URL: {url} to create device for extension: {extension}")
    print(f"Generated SIP Password: {sip_password}")  # Keep for terminal
    logger.info(f"Generated SIP Password: {sip_password}")
    print(f"Request payload: {json.dumps(data, indent=2)}")  # Keep for terminal
    logger.debug(f"Request payload: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Status Code: {response.status_code}")  # Keep for terminal
        logger.info(f"Status Code: {response.status_code} for device extension: {extension}")
        
        if response.status_code in [200, 201, 202]:
            print(f"Device for extension {extension} created successfully")  # Keep for terminal
            print(f"SIP Registration Password: {sip_password}")  # Keep for terminal
            print(f"Response: {response.text}")  # Keep for terminal
            logger.info(f"Device for extension {extension} created successfully with status code: {response.status_code}")
            logger.info(f"SIP Registration Password provided to user: {sip_password}")
        else:
            print(f"Failed to create device: {response.status_code}")  # Keep for terminal
            print(response.text)  # Keep for terminal
            logger.error(f"Failed to create device for extension {extension}: {response.status_code}")
            logger.debug(f"Response text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")  # Keep for terminal
        logger.error(f"Network error creating device for extension {extension}: {e}")

def create_device_prompt():
    """
    Prompt the user for inputs and create a device.
    """
    if not API_TOKEN:
        print("Error: API_TOKEN not found in environment variables.")  # Keep for terminal
        logger.error("API_TOKEN not found in environment variables")
        return
    
    while True:
        try:
            custID = input("Enter the customer domain (e.g., sgdemo): ").strip()
            if not custID:
                raise ValueError("Customer domain cannot be empty.")
            domain = input("Enter the domain name (e.g., sgdemo): ").strip()
            if not domain:
                raise ValueError("Domain name cannot be empty.")
            extension = validate_extension(input("Enter the user extension (ID): ").strip())
            logger.info(f"Customer domain entered: {custID}")
            logger.info(f"Domain name entered: {domain}")
            break
        except ValueError as e:
            print(f"Error: {e}. Please try again.")  # Keep for terminal
            logger.warning(f"Input validation error: {e}")
    
    create_device(custID, domain, extension)

if __name__ == "__main__":
    print("Starting device creation script")  # Keep for terminal
    logger.info("Starting device creation script")
    
    create_device_prompt()
    
    print("Device creation script completed")  # Keep for terminal
    logger.info("Device creation script completed")