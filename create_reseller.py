import requests
import json
import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

# Retrieve the API token
API_TOKEN = os.getenv("API_TOKEN")

print(API_TOKEN)


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
    print(f"Calling API URL: {url}")
    print(f"Headers being sent: {headers}")
    print(f"Data being sent: {data}")
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code in (201, 202):
        print("Reseller created successfully")
    else:
        print(f"Failed to create reseller: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    reseller_name = input("Enter the reseller name: ")
    description = input("Enter the description: ")
    # Make sure to pass the domain as well. Replace 'yourdomain' with the appropriate value.
    create_reseller("yourdomain", reseller_name, description)
