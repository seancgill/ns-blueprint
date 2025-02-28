import requests
import json
import os
import shutil
from dotenv import load_dotenv
from logging_setup import setup_logging
from create_image import create_image, process_images

# Initialize logger
logger = setup_logging()

# Load variables from the .env file into the environment
load_dotenv(override=True)

# Retrieve the API token
API_TOKEN = os.getenv("API_TOKEN")
print(f"Loaded API_TOKEN: {API_TOKEN}")
logger.info(f"Loaded API_TOKEN: {API_TOKEN}")

def create_reseller(custID, reseller, description="Training reseller created via API"):
    url = f"https://{custID}.trynetsapiens.com/ns-api/v2/resellers"
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "reseller": reseller,
        "description": description
    }
    print(f"Calling API URL: {url}")
    logger.info(f"Calling API URL: {url} to create reseller: {reseller}")
    print(f"Request payload: {json.dumps(data, indent=2)}")
    logger.debug(f"Request payload: {json.dumps(data, indent=2)}")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Status Code: {response.status_code}")
        logger.info(f"Status Code: {response.status_code} for reseller: {reseller}")
        if response.status_code in [200, 201, 202]:
            print(f"Reseller {reseller} created successfully")
            logger.info(f"Reseller '{reseller}' created successfully with status code: {response.status_code}")
        elif response.status_code == 409:
            print(f"Reseller {reseller} already exists, skipping.")
            logger.info(f"Reseller '{reseller}' already exists, skipping (Status: 409)")
        else:
            print(f"Failed to create reseller {reseller}: {response.status_code}")
            logger.error(f"Failed to create reseller '{reseller}': {response.status_code}")
        print(response.text)
        logger.debug(f"Response text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling {url}: {e}")
        logger.error(f"Error calling {url} to create reseller '{reseller}': {e}")

def create_domain(custID, domain, reseller, description, dial_plan, dial_policy):
    url = f"https://{custID}.trynetsapiens.com/ns-api/v2/domains"
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "domain": domain,
        "description": description,
        "dial-plan": dial_plan,
        "dial-policy": dial_policy,
        "area-code": "858",
        "caller-id-name": "Training CID",
        "caller-id-number": "8585551234",
        "caller-id-number-emergency": "8585551234",
        "reseller": reseller,
        "time-zone": "US/Pacific",
        "music-on-hold-enabled": "yes",
        "music-on-ring-enabled": "no",
        "music-on-hold-randomized-enabled": "no"
    }
    print(f"Calling API URL: {url}")
    logger.info(f"Calling API URL: {url} to create domain: {domain}")
    print(f"Request payload: {json.dumps(data, indent=2)}")
    logger.debug(f"Request payload: {json.dumps(data, indent=2)}")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Status Code: {response.status_code}")
        logger.info(f"Status Code: {response.status_code} for domain: {domain}")
        if response.status_code in [200, 201, 202]:
            print(f"Domain {domain} created successfully with dial plan {dial_plan}")
            logger.info(f"Domain '{domain}' created successfully with dial plan '{dial_plan}' with status code: {response.status_code}")
        else:
            print(f"Failed to create domain: {response.status_code}")
            logger.error(f"Failed to create domain '{domain}': {response.status_code}")
        print(response.text)
        logger.debug(f"Response text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling {url}: {e}")
        logger.error(f"Error calling {url} to create domain '{domain}': {e}")

def create_user(custID, domain, extension, first_name, last_name, email, user_scope):
    url = f"https://{custID}.trynetsapiens.com/ns-api/v2/domains/{domain}/users"
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "synchronous": "no",
        "user-scope": user_scope,
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
        "department": "Training Department",
        "site": "Training Site",
        "time-zone": "America/New_York",
        "voicemail-login-pin": 1818,
        "dial-plan": domain,
        "dial-policy": "US and Canada",
        "status-message": "Training user",
        "directory-name-number-dtmf-mapping": 564,
        "ring-no-answer-timeout-seconds": 30,
        "limits-max-data-storage-kilobytes": 10240,
        "limits-max-active-calls-total": 0,
        "directory-override-order-duplicate-dtmf-mapping": 0,
        "voicemail-greeting-index": 0,
        "caller-id-name": f"{first_name} {last_name}"
    }
    print(f"Calling API URL: {url}")
    logger.info(f"Calling API URL: {url} to create user: {first_name} {last_name} (Ext: {extension})")
    print(f"Request payload: {json.dumps(data, indent=2)}")
    logger.debug(f"Request payload: {json.dumps(data, indent=2)}")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Status Code: {response.status_code}")
        logger.info(f"Status Code: {response.status_code} for user: {first_name} {last_name} (Ext: {extension})")
        if response.status_code in [200, 201, 202]:
            print(f"User {first_name} {last_name} (Ext: {extension}, Scope: {user_scope}) created successfully")
            logger.info(f"User '{first_name} {last_name}' (Ext: {extension}, Scope: {user_scope}) created successfully with status code: {response.status_code}")
        else:
            print(f"Failed to create user: {response.status_code}")
            logger.error(f"Failed to create user '{first_name} {last_name}' (Ext: {extension}): {response.status_code}")
        print(response.text)
        logger.debug(f"Response text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling {url}: {e}")
        logger.error(f"Error calling {url} to create user '{first_name} {last_name}' (Ext: {extension}): {e}")

def create_device(custID, domain, extension):
    url = f"https://{custID}.trynetsapiens.com/ns-api/v2/domains/{domain}/users/{extension}/devices"
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "synchronous": "no",
        "caller-id-number-emergency": "8585551234",
        "device-force-notify-new-voicemails-enabled": "no",
        "device-level-call-recording-enabled": "yes",
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
        "device-provisioning-username": f"{extension}@{custID}",
        "device": extension
    }
    print(f"Calling API URL: {url}")
    logger.info(f"Calling API URL: {url} to create device for extension: {extension}")
    print(f"Request payload: {json.dumps(data, indent=2)}")
    logger.debug(f"Request payload: {json.dumps(data, indent=2)}")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Status Code: {response.status_code}")
        logger.info(f"Status Code: {response.status_code} for device extension: {extension}")
        if response.status_code in [200, 201, 202]:
            print(f"Device for extension {extension} created successfully")
            logger.info(f"Device for extension {extension} created successfully with status code: {response.status_code}")
        elif response.status_code == 409:
            print(f"Device for extension {extension} already exists, skipping.")
            logger.warning(f"Device for extension {extension} already exists, skipping (Status: 409)")
        else:
            print(f"Failed to create device: {response.status_code}")
            logger.error(f"Failed to create device for extension {extension}: {response.status_code}")
        print(response.text)
        logger.debug(f"Response text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling {url}: {e}")
        logger.error(f"Error calling {url} to create device for extension {extension}: {e}")

def create_call_park(custID, domain, callqueue, description):
    url = f"https://{custID}.trynetsapiens.com/ns-api/v2/domains/{domain}/callqueues"
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "synchronous": "no",
        "callqueue": callqueue,
        "description": description,
        "callqueue-dispatch-type": "Call Park",
        "callqueue-calculate-statistics": "no",
        "callqueue-agent-dispatch-timeout-seconds": 0,
        "callqueue-max-current-callers-to-accept-new-callers": 1,
        "callqueue-max-wait-timeout-minutes": 60,
        "site": "",
        "subscriber_group": ""
    }
    print(f"Calling API URL: {url}")
    logger.info(f"Calling API URL: {url} to create call park: {callqueue}")
    print(f"Request payload: {json.dumps(data, indent=2)}")
    logger.debug(f"Request payload: {json.dumps(data, indent=2)}")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Status Code: {response.status_code}")
        logger.info(f"Status Code: {response.status_code} for call park: {callqueue}")
        if response.status_code in [200, 201, 202]:
            print(f"Call park {callqueue} ({description}) created successfully")
            logger.info(f"Call park '{callqueue}' ({description}) created successfully with status code: {response.status_code}")
        elif response.status_code == 409:
            print(f"Call park {callqueue} already exists, attempting update")
            logger.info(f"Call park '{callqueue}' already exists, attempting update (Status: 409)")
            response = requests.put(url, headers=headers, data=json.dumps(data))
            print(f"PUT Status Code: {response.status_code} for updating call park: {callqueue}")
            logger.info(f"PUT Status Code: {response.status_code} for updating call park: {callqueue}")
        else:
            print(f"Failed to create call park {callqueue}: {response.status_code}")
            logger.error(f"Failed to create call park '{callqueue}': {response.status_code}")
        print(response.text)
        logger.debug(f"Response text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling {url}: {e}")
        logger.error(f"Error calling {url} to create call park '{callqueue}': {e}")

def create_call_queue(custID, domain, callqueue, description, dispatch_type="Ring All"):
    url = f"https://{custID}.trynetsapiens.com/ns-api/v2/domains/{domain}/callqueues"
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "synchronous": "no",
        "callqueue": callqueue,
        "description": description,
        "callqueue-dispatch-type": dispatch_type,
        "callqueue-calculate-statistics": "yes",
        "callqueue-agent-dispatch-timeout-seconds": 12,
        "callqueue-force-full-intro-playback": "no"
    }
    print(f"Calling API URL: {url}")
    logger.info(f"Calling API URL: {url} to create call queue: {callqueue}")
    print(f"Request payload: {json.dumps(data, indent=2)}")
    logger.debug(f"Request payload: {json.dumps(data, indent=2)}")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Status Code: {response.status_code}")
        logger.info(f"Status Code: {response.status_code} for call queue: {callqueue}")
        if response.status_code in [200, 201, 202]:
            print(f"Call queue {callqueue} ({description}) created successfully")
            logger.info(f"Call queue '{callqueue}' ({description}) created successfully with status code: {response.status_code}")
        elif response.status_code == 409:
            print(f"Call queue {callqueue} already exists, skipping")
            logger.info(f"Call queue '{callqueue}' already exists, skipping (Status: 409)")
        else:
            print(f"Failed to create call queue {callqueue}: {response.status_code}")
            logger.error(f"Failed to create call queue '{callqueue}': {response.status_code}")
        print(response.text)
        logger.debug(f"Response text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling {url}: {e}")
        logger.error(f"Error calling {url} to create call queue '{callqueue}': {e}")

def add_agent_to_call_queue(custID, domain, callqueue, agent_extension):
    url = f"https://{custID}.trynetsapiens.com/ns-api/v2/domains/{domain}/callqueues/{callqueue}/agents"
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    agent_id = f"{agent_extension}@{domain}"

    # Check if agent is already in the queue
    print(f"Checking if agent {agent_extension} is already in call queue {callqueue}")
    logger.info(f"Checking if agent {agent_extension} is already in call queue {callqueue}")
    try:
        get_response = requests.get(url, headers=headers)
        if get_response.status_code == 200:
            agents = get_response.json()
            for agent in agents:
                if agent.get("callqueue-agent-id") == agent_id:
                    print(f"Agent {agent_extension} already exists in call queue {callqueue}, skipping")
                    logger.info(f"Agent '{agent_extension}' already exists in call queue '{callqueue}', skipping")
                    return  # Skip adding if agent is found
        else:
            print(f"Failed to fetch agents for queue {callqueue}: {get_response.status_code}")
            logger.warning(f"Failed to fetch agents for queue {callqueue}: {get_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error checking agents for queue {callqueue}: {e}")
        logger.error(f"Error checking agents for queue {callqueue}: {e}")

    # Add agent if not found
    data = {
        "synchronous": "no",
        "callqueue-agent-wrap-up-allowance-seconds": 0,
        "auto-answer-enabled": "no",
        "callqueue-agent-answer-confirmation-enabled": "no",
        "callqueue-agent-id": agent_id,
        "callqueue": callqueue,
        "domain": domain
    }
    print(f"Calling API URL: {url} to add agent {agent_extension} to call queue: {callqueue}")
    logger.info(f"Calling API URL: {url} to add agent {agent_extension} to call queue: {callqueue}")
    print(f"Request payload: {json.dumps(data, indent=2)}")
    logger.debug(f"Request payload: {json.dumps(data, indent=2)}")
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Status Code: {response.status_code}")
        logger.info(f"Status Code: {response.status_code} for adding agent {agent_extension} to call queue: {callqueue}")
        if response.status_code in [200, 201, 202]:
            print(f"Agent {agent_extension} added to call queue {callqueue} successfully")
            logger.info(f"Agent '{agent_extension}' added to call queue '{callqueue}' successfully with status code: {response.status_code}")
        else:
            print(f"Failed to add agent {agent_extension} to call queue {callqueue}: {response.status_code}")
            logger.error(f"Failed to add agent '{agent_extension}' to call queue '{callqueue}': {response.status_code}")
        print(response.text)
        logger.debug(f"Response text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling {url}: {e}")
        logger.error(f"Error calling {url} to add agent '{agent_extension}' to call queue '{callqueue}': {e}")

def create_training_domains(custID):
    resellers = [
        {"name": "training_reseller1", "description": "Training reseller 1 created via API", "image_path": "reseller_images/reseller-one-logo.jpeg"},
        {"name": "training_reseller2", "description": "Training reseller 2 created via API", "image_path": "reseller_images/reseller-two-logo.jpg"}
    ]
    domains = [
        {"name": "trainingdomain1", "reseller": "training_reseller1"},
        {"name": "trainingdomain2", "reseller": "training_reseller2"}
    ]
    description = "Training domain created via API"
    dial_policy = "US and Canada"

    call_parks = [
        {"callqueue": "701", "description": "Park One"},
        {"callqueue": "702", "description": "Park Two"},
        {"callqueue": "703", "description": "Park Three"}
    ]
    call_queues = [
        {"callqueue": "801", "description": "Queue One"},
        {"callqueue": "802", "description": "Queue Two"}
    ]
    agent_extensions = ["2004", "2005"]
    user_scopes = [
        "Call Center Agent", "Call Center Agent", "Simple User", "Basic User",
        "Advanced User", "Call Center Supervisor", "Office Manager", "Reseller"
    ]
    users = [
        {"extension": "2004", "email": "cc.agent1@example.com"},
        {"extension": "2005", "email": "cc.agent2@example.com"},
        {"extension": "2000", "email": "simple.user@example.com"},
        {"extension": "2001", "email": "basic.user@example.com"},
        {"extension": "2002", "email": "advanced.user@example.com"},
        {"extension": "2003", "email": "cc.supervisor@example.com"},
        {"extension": "2006", "email": "office.manager@example.com"},
        {"extension": "2007", "email": "reseller@example.com"}
    ]

    # Create resellers and process images
    print(f"\n=== Creating resellers for {custID} ===")
    logger.info(f"=== Creating resellers for {custID} ===")
    for reseller_info in resellers:
        reseller_name = reseller_info["name"]
        create_reseller(custID, reseller_name, reseller_info["description"])
        print(f"\n=== Processing images for reseller {reseller_name} ===")
        logger.info(f"=== Processing images for reseller {reseller_name} ===")
        image_dir = "image_files"
        if os.path.exists(image_dir):
            shutil.rmtree(image_dir)
            os.makedirs(image_dir)
            print(f"Cleared {image_dir} for {reseller_name}")
            logger.info(f"Cleared {image_dir} for {reseller_name}")
        process_images(reseller_info["image_path"], custID, reseller_name, local=True)

    # Create domains with dial plans matching domain names
    print(f"\n=== Creating domain: {custID} with reseller: {custID}_reseller ===")
    logger.info(f"=== Creating domain: {custID} with reseller: {custID}_reseller ===")
    create_domain(custID, custID, f"{custID}_reseller", 'made via api', custID, dial_policy)

    for domain_info in domains:
        domain = domain_info["name"]
        reseller = domain_info["reseller"]
        print(f"\n=== Creating domain: {domain} with reseller: {reseller} ===")
        logger.info(f"=== Creating domain: {domain} with reseller: {reseller} ===")
        create_domain(custID, domain, reseller, description, domain, dial_policy)

        print(f"\n=== Creating users and devices for {domain} ===")
        logger.info(f"=== Creating users and devices for {domain} ===")
        for i, user in enumerate(users):
            scope = user_scopes[i]
            scope_parts = scope.split(" ")
            first_name = scope_parts[0]
            last_name = "User" if len(scope_parts) == 1 else " ".join(scope_parts[1:])
            print(f"\nCreating user {user['extension']} with scope {scope}")
            logger.info(f"Creating user {user['extension']} with scope {scope}")
            create_user(custID, domain, user["extension"], first_name, last_name, user["email"], scope)
            create_device(custID, domain, user["extension"])

        print(f"\n=== Creating call parks for {domain} ===")
        logger.info(f"=== Creating call parks for {domain} ===")
        for park in call_parks:
            create_call_park(custID, domain, park["callqueue"], park["description"])

        print(f"\n=== Creating call queues for {domain} ===")
        logger.info(f"=== Creating call queues for {domain} ===")
        for queue in call_queues:
            create_call_queue(custID, domain, queue["callqueue"], queue["description"])

        print(f"\n=== Adding agents to call queues for {domain} ===")
        logger.info(f"=== Adding agents to call queues for {domain} ===")
        for queue in call_queues:
            for agent_extension in agent_extensions:
                add_agent_to_call_queue(custID, domain, queue["callqueue"], agent_extension)

if __name__ == "__main__":
    print("Starting training domains creation script")
    logger.info("Starting training domains creation script")
    custID = input("Enter the customer domain (e.g., sgdemo): ").strip()
    logger.info(f"Customer domain entered: {custID}")
    create_training_domains(custID)
    print("Training domains creation script completed")
    logger.info("Training domains creation script completed")