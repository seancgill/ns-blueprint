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

print(API_TOKEN)  # Keep for terminal
logger.info(f"Loaded API_TOKEN: {API_TOKEN}")  # Log to file and terminal

def create_reseller(domain, reseller_name, description):
    url = f"https://{domain}.trynetsapiens.com/ns-api/v2/resellers"
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "reseller": reseller_name,
        "description": description
    }
    
    # Log the API URL being called
    print(f"Calling API URL: {url}")  # Keep for terminal
    logger.info(f"Calling API URL: {url}")
    print(f"Headers being sent: {headers}")  # Keep for terminal
    logger.debug(f"Headers being sent: {json.dumps(headers, indent=2)}")  # Use debug for detailed output
    print(f"Data being sent: {data}")  # Keep for terminal
    logger.debug(f"Data being sent: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code in (201, 202):
        print("Reseller created successfully")  # Keep for terminal
        logger.info(f"Reseller {reseller_name} created successfully with status code: {response.status_code}")
    else:
        print(f"Failed to create reseller: {response.status_code}")  # Keep for terminal
        logger.error(f"Failed to create reseller {reseller_name}: {response.status_code}")
        print(response.text)  # Keep for terminal
        logger.debug(f"Response text: {response.text}")

if __name__ == "__main__":
    print("Starting reseller creation script")  # Keep for terminal
    logger.info("Starting reseller creation script")
    
    reseller_name = input("Enter the reseller name: ")
    description = input("Enter the description: ")
    domain = input("Enter the domain (e.g., sgdemo): ")  # Added domain input to replace 'yourdomain'
    logger.info(f"Reseller name entered: {reseller_name}")
    logger.info(f"Description entered: {description}")
    logger.info(f"Domain entered: {domain}")
    
    create_reseller(domain, reseller_name, description)
    
    print("Reseller creation script completed")  # Keep for terminal
    logger.info("Reseller creation script completed")