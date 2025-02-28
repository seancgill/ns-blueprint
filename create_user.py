import requests
import json
import os
import re
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

def validate_extension(extension):
    """Check if extension is numeric."""
    if not extension.isdigit():
        raise ValueError("Extension must be numeric (e.g., 1001).")
    logger.info(f"Validated extension: {extension}")
    return extension

def validate_email(email):
    """Basic email format validation."""
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_pattern.match(email):
        raise ValueError("Invalid email format (e.g., user@domain.com).")
    logger.info(f"Validated email: {email}")
    return email

def validate_name(name, field_name):
    """Check if name is non-empty."""
    if not name:
        raise ValueError(f"{field_name} cannot be empty.")
    logger.info(f"Validated {field_name.lower()}: {name}")
    return name

def create_user(custID, domain):
    """
    Create a user in the NetSapiens API with input validation.
    Args:
        custID (str): Customer ID (e.g., 'sgdemo')
        domain (str): Domain name (e.g., 'sgdemo')
    """
    while True:
        try:
            extension = validate_extension(input("Enter the user extension (ID): ").strip())
            first_name = validate_name(input("Enter the first name: ").strip(), "First name")
            last_name = validate_name(input("Enter the last name: ").strip(), "Last name")
            email = validate_email(input("Enter the email address: ").strip())
            break  # Exit loop if all inputs are valid
        except ValueError as e:
            print(f"Error: {e}. Please try again.")  # Keep for terminal
            logger.warning(f"Input validation error: {e}")

    url = f"https://{custID}.trynetsapiens.com/ns-api/v2/domains/{domain}/users"
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "synchronous": "no",
        "user-scope": "Super User",
        "privacy": "no",
        "voicemail-user-control-enabled": "yes",
        "phone-numbers-to-allow-enabled": "yes",
        "phone-numbers-to-reject-enabled": "yes",
        "call-screening-enabled": "no",
        "language-token": "en_US",
        "directory-annouce-in-dial-by-name-enabled": "yes",
        "voicemail-enabled": "yes",
        "voicemail-receive-broadcast-enabled": "yes",
        "reject-anonymous-calls-enabled": "no",
        "voicemail-playback-announce-datetime-received": "no",
        "voicemail-playback-announce-caller-id": "no",
        "voicemail-playback-sort-newest-to-oldest": "yes",
        "email-send-alert-new-voicemail-behavior": "no",
        "email-send-alert-new-voicemail-enabled": "no",
        "email-send-alert-new-missed-call-enabled": "no",
        "email-send-alert-data-storage-limit-reached-enabled": "no",
        "directory-name-visible-in-list-enabled": "yes",
        "voicemail-transcription-enabled": "no",
        "call-recordings-hide-from-others-enabled": "no",
        "music-on-hold-randomized-enabled": "no",
        "recording-configuration": "no",
        "user": extension,
        "name-first-name": first_name,
        "name-last-name": last_name,
        "login-username": extension,
        "email-address": email,
        "department": "Support Department",
        "site": "Site One",
        "time-zone": "America/New_York",
        "voicemail-login-pin": 1818,
        "dial-plan": domain,
        "dial-policy": "US and Canada",
        "status-message": "my status message",
        "directory-name-number-dtmf-mapping": 564,
        "ring-no-answer-timeout-seconds": 30,
        "limits-max-data-storage-kilobytes": 10240,
        "limits-max-active-calls-total": 0,
        "directory-override-order-duplicate-dtmf-mapping": 0,
        "voicemail-greeting-index": 0,
        "caller-id-name": f"{first_name} {last_name}"
    }
    
    print(f"Calling API URL: {url}")  # Keep for terminal
    logger.info(f"Calling API URL: {url} to create user: {first_name} {last_name} (Ext: {extension})")
    print(f"Request payload: {json.dumps(data, indent=2)}")  # Keep for terminal
    logger.debug(f"Request payload: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        print(f"Status Code: {response.status_code}")  # Keep for terminal
        logger.info(f"Status Code: {response.status_code} for user: {first_name} {last_name} (Ext: {extension})")
        
        if response.status_code in [200, 201, 202]:
            print(f"User {first_name} {last_name} (Ext: {extension}) created successfully")  # Keep for terminal
            logger.info(f"User '{first_name} {last_name}' (Ext: {extension}) created successfully with status code: {response.status_code}")
        else:
            print(f"Failed to create user: {response.status_code}")  # Keep for terminal
            print(response.text)  # Keep for terminal
            logger.error(f"Failed to create user '{first_name} {last_name}' (Ext: {extension}): {response.status_code}")
            logger.debug(f"Response text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling {url}: {e}")  # Keep for terminal
        logger.error(f"Error calling {url} to create user '{first_name} {last_name}' (Ext: {extension}): {e}")

if __name__ == "__main__":
    print("Starting user creation script")  # Keep for terminal
    logger.info("Starting user creation script")
    
    custID = input("Enter the customer domain (e.g., sgdemo): ").strip()
    domain = input("Enter the domain name (e.g., sgdemo): ").strip()
    logger.info(f"Customer domain entered: {custID}")
    logger.info(f"Domain name entered: {domain}")
    
    create_user(custID, domain)
    
    print("User creation script completed")  # Keep for terminal
    logger.info("User creation script completed")