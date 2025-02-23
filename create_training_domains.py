import requests
import json
import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv(override=True)

# Retrieve the API token
API_TOKEN = os.getenv("API_TOKEN")
print(f"Loaded API_TOKEN: {API_TOKEN}")

def create_reseller(custID, reseller, description="Training reseller created via API"):
    """Create a reseller in the NetSapiens API."""
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
    print(f"Request payload: {json.dumps(data, indent=2)}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201, 202]:
        print(f"Reseller {reseller} created successfully")
    else:
        print(f"Failed to create reseller {reseller}: {response.status_code}")
    print(response.text)

def create_domain(custID, domain, reseller, description, dial_plan, dial_policy):
    """Create a domain in the NetSapiens API."""
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
    print(f"Request payload: {json.dumps(data, indent=2)}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201, 202]:
        print(f"Domain {domain} created successfully")
    else:
        print(f"Failed to create domain: {response.status_code}")
    print(response.text)

def create_user(custID, domain, extension, first_name, last_name, email, user_scope):
    """Create a user in the NetSapiens API with a specific user scope."""
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
    print(f"Request payload: {json.dumps(data, indent=2)}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201, 202]:
        print(f"User {first_name} {last_name} (Ext: {extension}, Scope: {user_scope}) created successfully")
    else:
        print(f"Failed to create user: {response.status_code}")
    print(response.text)

def create_device(custID, domain, extension):
    """Create a device for a user in the NetSapiens API."""
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
        "device-push-enabled": "yes",
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
    print(f"Request payload: {json.dumps(data, indent=2)}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201, 202]:
        print(f"Device for extension {extension} created successfully")
    elif response.status_code == 409:
        print(f"Device for extension {extension} already exists, skipping.")
    else:
        print(f"Failed to create device: {response.status_code}")
    print(response.text)

def create_call_park(custID, domain, callqueue, description):
    """Create a call park in the NetSapiens API."""
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
        "callqueue-dispatch-type": "Call Park"
    }
    
    print(f"Calling API URL: {url}")
    print(f"Request payload: {json.dumps(data, indent=2)}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201, 202]:
        print(f"Call park {callqueue} ({description}) created successfully")
    else:
        print(f"Failed to create call park {callqueue}: {response.status_code}")
    print(response.text)

def create_call_queue(custID, domain, callqueue, description, dispatch_type="Ring All"):
    """Create a call queue in the NetSapiens API."""
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
    print(f"Request payload: {json.dumps(data, indent=2)}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201, 202]:
        print(f"Call queue {callqueue} ({description}) created successfully")
    else:
        print(f"Failed to create call queue {callqueue}: {response.status_code}")
    print(response.text)

def add_agent_to_call_queue(custID, domain, callqueue, agent_extension):
    """Add an agent to a call queue in the NetSapiens API."""
    url = f"https://{custID}.trynetsapiens.com/ns-api/v2/domains/{domain}/callqueues/{callqueue}/agents"
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        "synchronous": "no",
        "callqueue-agent-wrap-up-allowance-seconds": 0,
        "auto-answer-enabled": "no",
        "callqueue-agent-answer-confirmation-enabled": "no",
        "callqueue-agent-id": agent_extension,
        "callqueue": callqueue,
        "domain": domain
    }
    
    print(f"Calling API URL: {url}")
    print(f"Request payload: {json.dumps(data, indent=2)}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201, 202]:
        print(f"Agent {agent_extension} added to call queue {callqueue} successfully")
    else:
        print(f"Failed to add agent {agent_extension} to call queue {callqueue}: {response.status_code}")
    print(response.text)

def create_training_domains(custID):
    """Create two hardcoded training domains with resellers, users (including two call center agents at 2004 and 2005), devices, call parks, and call queues with agents."""
    resellers = [
        {"name": "training_reseller1", "description": "Training reseller 1 created via API"},
        {"name": "training_reseller2", "description": "Training reseller 2 created via API"}
    ]
    domains = [
        {"name": "trainingdomain1", "reseller": "training_reseller1"},
        {"name": "trainingdomain2", "reseller": "training_reseller2"}
    ]
    description = "Training domain created via API"
    dial_plan = custID
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

    agent_extensions = ["2004", "2005"]  # The two call center agents

    user_scopes = [
        "Call Center Agent",  # For 2004
        "Call Center Agent",  # For 2005
        "Simple User",
        "Basic User",
        "Advanced User",
        "Call Center Supervisor",
        "Office Manager",
        "Reseller"
    ]

    users = [
        {"extension": "2004", "email": "cc.agent1@netsapiens.com"},  # First agent
        {"extension": "2005", "email": "cc.agent2@netsapiens.com"},  # Second agent
        {"extension": "2000", "email": "simple.user@netsapiens.com"},
        {"extension": "2001", "email": "basic.user@netsapiens.com"},
        {"extension": "2002", "email": "advanced.user@netsapiens.com"},
        {"extension": "2003", "email": "cc.supervisor@netsapiens.com"},
        {"extension": "2006", "email": "office.manager@netsapiens.com"},
        {"extension": "2007", "email": "reseller@netsapiens.com"}
    ]

    # Create resellers first
    print(f"\n=== Creating resellers for {custID} ===")
    for reseller_info in resellers:
        create_reseller(custID, reseller_info["name"], reseller_info["description"])

    # Then create domains and everything else
    for domain_info in domains:
        domain = domain_info["name"]
        reseller = domain_info["reseller"]
        print(f"\n=== Creating domain: {domain} with reseller: {reseller} ===")
        create_domain(custID, domain, reseller, description, dial_plan, dial_policy)
        
        print(f"\n=== Creating users and devices for {domain} ===")
        for i, user in enumerate(users):
            scope = user_scopes[i]
            scope_parts = scope.split(" ")
            if len(scope_parts) == 1:  # Single-word scope
                first_name = scope_parts[0]
                last_name = "User"
            else:  # Multi-word scope
                first_name = scope_parts[0]
                last_name = " ".join(scope_parts[1:])
            
            print(f"\nCreating user {user['extension']} with scope {scope}")
            create_user(
                custID, domain, user["extension"], first_name,
                last_name, user["email"], scope
            )
            create_device(custID, domain, user["extension"])
        
        print(f"\n=== Creating call parks for {domain} ===")
        for park in call_parks:
            create_call_park(custID, domain, park["callqueue"], park["description"])
        
        print(f"\n=== Creating call queues for {domain} ===")
        for queue in call_queues:
            create_call_queue(custID, domain, queue["callqueue"], queue["description"])
        
        print(f"\n=== Adding agents to call queues for {domain} ===")
        for queue in call_queues:
            for agent_extension in agent_extensions:
                add_agent_to_call_queue(custID, domain, queue["callqueue"], agent_extension)

if __name__ == "__main__":
    custID = input("Enter the customer domain (e.g., sgdemo): ").strip()
    create_training_domains(custID)