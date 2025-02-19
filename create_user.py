import requests
import json
import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

# Retrieve the API token
API_TOKEN = os.getenv("API_TOKEN")

def create_user(custID, domain, extension, first_name, last_name, email):
    url = f"https://{custID}.trynetsapiens.com/ns-api/v2/domains/{custID}/users"
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "synchronous": "no",
        "user-scope": "Basic User",
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
        "dial-policy": "US & Canada",
        "status-message": "my status message",
        "directory-name-number-dtmf-mapping": 564,
        "ring-no-answer-timeout-seconds": 30,
        "limits-max-data-storage-kilobytes": 10240,
        "limits-max-active-calls-total": 0,
        "directory-override-order-duplicate-dtmf-mapping": 0,
        "voicemail-greeting-index": 0,
        "caller-id-name": f"{first_name} {last_name}"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code in [200, 201, 202]:
        print("Domain created successfully")
    else:
        print(f"Failed to create domain: {response.status_code}")
    print(response.text)

if __name__ == "__main__":
    custID = input("Enter the customer domain (e.g., sgdemo): ").strip()
    domain = input("Enter the customer domain (e.g., sgdemo): ").strip()
    extension = input("Enter the user extension (ID): ").strip()
    first_name = input("Enter the first name: ").strip()
    last_name = input("Enter the last name: ").strip()
    email = input("Enter the email address: ").strip()
    
    create_user(custID, domain, extension, first_name, last_name, email)