import requests
import json
import os
from dotenv import load_dotenv
from logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# Load variables from the .env file into the environment
load_dotenv()

# Retrieve the API token
API_TOKEN = os.getenv("API_TOKEN")

print(f"Loaded API_TOKEN: {API_TOKEN}")  # Keep for terminal
logger.info(f"Loaded API_TOKEN: {API_TOKEN}")

def create_domain(custID, domain, reseller, description, dial_plan, dial_policy, area_code, caller_id_name, caller_id_number, caller_id_number_emergency):
    url = f"https://{custID}.trynetsapiens.com/ns-api/v2/domains"
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "synchronous": "yes",
        "recording-configuration": "yes",
        "voicemail-transcription-enabled": "deepgram",
        "language-token": "en_US",
        "domain": domain,
        "reseller": reseller,
        "description": description,
        "domain-type": "Standard",
        "dial-plan": dial_plan,
        "dial-policy": dial_policy,
        "email-send-from-address": "voicemail@netsapiens.com",
        "single-sign-on-enabled": "no",
        "area-code": area_code,
        "caller-id-name": caller_id_name,
        "caller-id-number": caller_id_number,
        "caller-id-number-emergency": caller_id_number_emergency,
        "voicemail-enabled": "yes",
        "is-domain-locked": "no",
        "is-stir-enabled": "no",
        "is-ivr-forward-change-blocked": "no"
    }
    
    print(f"Calling API URL: {url}")  # Keep for terminal
    logger.info(f"Calling API URL: {url} to create domain: {domain}")
    logger.debug(f"Payload: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code in [200, 201, 202]:
            print("Domain created successfully")  # Keep for terminal
            logger.info(f"Domain '{domain}' created successfully with status code: {response.status_code}")
        else:
            print(f"Failed to create domain: {response.status_code}")  # Keep for terminal
            logger.error(f"Failed to create domain '{domain}': {response.status_code}")
        
        print(response.text)  # Keep for terminal
        logger.debug(f"Response text: {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling {url}: {e}")  # Keep for terminal
        logger.error(f"Error calling {url} to create domain '{domain}': {e}")

if __name__ == "__main__":
    print("Starting domain creation script")  # Keep for terminal
    logger.info("Starting domain creation script")
    
    # Example inputs (you can modify these or prompt the user)
    custID = input("Enter the customer ID (e.g., sgdemo): ").strip()
    domain = input("Enter the domain name: ").strip()
    reseller = input("Enter the reseller name: ").strip()
    description = input("Enter the description: ").strip()
    dial_plan = input("Enter the dial plan: ").strip()
    dial_policy = input("Enter the dial policy: ").strip()
    area_code = input("Enter the area code: ").strip()
    caller_id_name = input("Enter the caller ID name: ").strip()
    caller_id_number = input("Enter the caller ID number: ").strip()
    caller_id_number_emergency = input("Enter the emergency caller ID number: ").strip()
    
    logger.info(f"Customer ID entered: {custID}")
    logger.info(f"Domain entered: {domain}")
    logger.info(f"Reseller entered: {reseller}")
    logger.info(f"Description entered: {description}")
    logger.info(f"Dial plan entered: {dial_plan}")
    logger.info(f"Dial policy entered: {dial_policy}")
    logger.info(f"Area code entered: {area_code}")
    logger.info(f"Caller ID name entered: {caller_id_name}")
    logger.info(f"Caller ID number entered: {caller_id_number}")
    logger.info(f"Emergency caller ID number entered: {caller_id_number_emergency}")
    
    create_domain(custID, domain, reseller, description, dial_plan, dial_policy, area_code, caller_id_name, caller_id_number, caller_id_number_emergency)
    
    print("Domain creation script completed")  # Keep for terminal
    logger.info("Domain creation script completed")