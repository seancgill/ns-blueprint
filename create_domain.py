import requests
import json
import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

# Retrieve the API token
API_TOKEN = os.getenv("API_TOKEN")

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
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code in [200, 201, 202]:
        print("Domain created successfully")
    else:
        print(f"Failed to create domain: {response.status_code}")
    print(response.text)