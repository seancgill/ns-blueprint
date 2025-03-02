# route_manager.py

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

print(f"Loaded API_TOKEN: {API_TOKEN}")  # Keep for terminal
logger.info(f"Loaded API_TOKEN: {API_TOKEN}")

def create_us_domestic_route(custID, match_to="sip:1??????????@*", con_host="a.icr.commio.com", con_index="1"):
    """
    Create a new route for US domestic calls pointing to the ThinQ LCR Outbound connection.
    
    Parameters:
      - custID: The host ID (e.g., 'sgdemo')
      - match_to: The pattern to match (default: US domestic numbers)
      - con_host: The target connection host (default: ThinQ LCR Outbound)
      - con_index: The connection index (default: "1")
    
    Returns:
      - The response from the API
    """
    url = f"https://api.{custID}.ucaas.tech/ns-api/v2/routecon"
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

    print(f"Creating route at: {url}")  # Keep for terminal
    logger.info(f"Creating route at: {url}")
    logger.debug(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")  # Keep for terminal
        logger.info(f"Status Code: {response.status_code} for route creation")
        logger.debug(f"Response text: {response.text}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating route at {url}: {e}")
        print(f"Error creating route at {url}: {e}")  # Keep for terminal
        raise

def manage_us_domestic_route(custID):
    """
    Main function to manage the US domestic route by creating it to point to ThinQ LCR Outbound.
    
    Parameters:
      - custID: The host ID (e.g., 'sgdemo')
    """
    print("Starting US domestic route management")  # Keep for terminal
    logger.info("Starting US domestic route management")

    # Create the route for US domestic calls
    response = create_us_domestic_route(custID)
    if response.status_code in (201, 202):
        print("US Domestic route created successfully to ThinQ LCR Outbound")  # Keep for terminal
        logger.info(f"US Domestic route created successfully with status code: {response.status_code}")
    elif response.status_code == 409:
        print("Route already exists. No changes made.")  # Keep for terminal
        logger.info("Route already exists. No changes made.")
    else:
        print(f"Failed to create US Domestic route: {response.status_code} - {response.text}")  # Keep for terminal
        logger.error(f"Failed to create US Domestic route: {response.status_code} - {response.text}")

    print("US domestic route management completed")  # Keep for terminal
    logger.info("US domestic route management completed")

if __name__ == "__main__":
    print("Starting route management script")  # Keep for terminal
    logger.info("Starting route management script")

    custID = input("Enter the host ID (e.g., sgdemo): ").strip()
    logger.info(f"Host ID entered: {custID}")

    manage_us_domestic_route(custID)