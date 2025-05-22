import requests
import json
import os
from dotenv import load_dotenv
from logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

# Load environment variables from .env file
load_dotenv()

# Retrieve the API token
API_TOKEN = os.getenv("API_TOKEN")

print(f"Loaded API_TOKEN: {API_TOKEN}")
logger.info(f"Loaded API_TOKEN: {API_TOKEN}")

def create_us_domestic_route(custID, api_url, match_to="sip:1??????????@*", con_host="a.icr.commio.com", con_index="1"):
    api_url = api_url.rstrip('/')
    url = f"{api_url}/ns-api/v2/routecon"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_TOKEN}",
        "content-type": "application/json"
    }
    payload = {
        "match_to": match_to,
        "con_index": con_index,
        "con_host": con_host
    }

    print(f"Creating route at: {url}")
    logger.info(f"Creating route at: {url}")
    logger.debug(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        logger.info(f"Status Code: {response.status_code} for route creation")
        logger.debug(f"Response text: {response.text}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating route at {url}: {e}")
        print(f"Error creating route at {url}: {e}")
        raise

def manage_us_domestic_route(custID, api_url):
    print("Starting US domestic route management")
    logger.info("Starting US domestic route management")

    response = create_us_domestic_route(custID, api_url)
    if response.status_code in (201, 202):
        print("US Domestic route created successfully to ThinQ LCR Outbound")
        logger.info(f"US Domestic route created successfully with status code: {response.status_code}")
    elif response.status_code == 409:
        print("Route already exists. No changes made.")
        logger.info("Route already exists. No changes made.")
    else:
        print(f"Failed to create US Domestic route: {response.status_code} - {response.text}")
        logger.error(f"Failed to create US Domestic route: {response.status_code} - {response.text}")

    print("US domestic route management completed")
    logger.info("US domestic route management completed")

if __name__ == "__main__":
    import re
    print("Starting route management script")
    logger.info("Starting route management script")

    custID = input("Enter the host ID (e.g., sgdemo): ").strip()
    api_url = input("Enter the full API URL (e.g., https://api.example.ucaas.tech): ").strip()
    
    if not re.match(r"^https?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", api_url):
        print("Invalid API URL. Please enter a valid URL (e.g., https://api.example.ucaas.tech).")
        logger.error(f"Invalid API URL provided: {api_url}")
        exit(1)
    
    logger.info(f"Host ID entered: {custID}")
    logger.info(f"API URL entered: {api_url}")

    manage_us_domestic_route(custID, api_url)