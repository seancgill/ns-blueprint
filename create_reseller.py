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

print(API_TOKEN)
logger.info(f"Loaded API_TOKEN: {API_TOKEN}")

def create_reseller(custID, reseller_name, description, api_url):
    url = f"{api_url}/ns-api/v2/resellers"
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "reseller": reseller_name,
        "description": description
    }
    
    print(f"Calling API URL: {url}")
    logger.info(f"Calling API URL: {url}")
    print(f"Headers being sent: {headers}")
    logger.debug(f"Headers being sent: {json.dumps(headers, indent=2)}")
    print(f"Data being sent: {data}")
    logger.debug(f"Data being sent: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code in (201, 202):
        print("Reseller created successfully")
        logger.info(f"Reseller {reseller_name} created successfully with status code: {response.status_code}")
    else:
        print(f"Failed to create reseller: {response.status_code}")
        logger.error(f"Failed to create reseller {reseller_name}: {response.status_code}")
        print(response.text)
        logger.debug(f"Response text: {response.text}")

if __name__ == "__main__":
    print("Starting reseller creation script")
    logger.info("Starting reseller creation script")
    
    reseller_name = input("Enter the reseller name: ")
    description = input("Enter the description: ")
    custID = input("Enter the custID (e.g., sgdemo): ")
    api_url = input("Enter the full API URL (e.g., https://api.example.ucaas.tech): ").strip()
    logger.info(f"Reseller name entered: {reseller_name}")
    logger.info(f"Description entered: {description}")
    logger.info(f"custID entered: {custID}")
    logger.info(f"API URL entered: {api_url}")
    
    create_reseller(custID, reseller_name, description, api_url)
    
    print("Reseller creation script completed")
    logger.info("Reseller creation script completed")