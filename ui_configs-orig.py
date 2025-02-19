import json
import requests
import os
import re
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

# Retrieve the API token
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("Missing API token. Set NETSAPIENS_API_TOKEN as an environment variable.")

# List of UI configurations that require user input
UI_CONFIGS_TO_PROMPT = {
    "PORTAL_CSS_PRIMARY_1": "Dark Blue",
    "PORTAL_CSS_PRIMARY_2": "Green",
    "PORTAL_CSS_COLOR_MENU_BAR_PRIMARY_1": "Gray",
    "PORTAL_CSS_COLOR_MENU_BAR_PRIMARY_2": "Dark Blue",
    "PORTAL_WEBPHONE_PWA_BACKGROUND_COLOR": "Gray",
    "PORTAL_WEBPHONE_PWA_THEME_COLOR": "Green",
    "PORTAL_THEME_ACCENT": "Green",
}

# Common payload fields
common_payload = {
    "admin-ui-account-type": "*",
    "reseller": "*",
    "user": "*",
    "user-scope": "*",
    "core-server": "*",
    "domain": "*",
    "description": "Created via API"
}

# Common headers for all API calls
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {API_TOKEN}",
    "content-type": "application/json"
}

def get_api_url(customer_name):
    # Adjust the URL pattern as needed.
    return f"https://{customer_name}.trynetsapiens.com/ns-api/v2/configurations"

def load_configurations(filename, customer_name):
    """Load configuration data from a JSON file and replace 'custID' with customer_name."""
    with open(filename, 'r') as file:
        configs = json.load(file)
    
    for config in configs:
        if isinstance(config.get("config_value"), str):
            config["config_value"] = config["config_value"].replace("custID", customer_name)
    return configs

def post_configuration(config, api_url):
    """Send the configuration to the API using the given API URL via POST."""
    payload = common_payload.copy()
    payload["config-name"] = config["config_name"]
    payload["config-value"] = config["config_value"]
    
    response = requests.post(api_url, headers=headers, json=payload)
    print(f"POST status code for {config['config_name']}: {response.status_code}")
    return response

def put_configuration(config, api_url):
    """Update the configuration using PUT."""
    payload = common_payload.copy()
    payload["config-name"] = config["config_name"]
    payload["config-value"] = config["config_value"]
    
    response = requests.put(api_url, headers=headers, json=payload)
    print(f"PUT status code for {config['config_name']}: {response.status_code}")
    return response



def is_valid_hex(color):
    """Check if input is a valid hex color code."""
    return bool(re.fullmatch(r"^#([A-Fa-f0-9]{6})$", color))

def prompt_for_color(config_name, current_value, color_description):
    """Prompt user for a new hex color, validate input, and return the new value."""
    while True:
        new_value = input(f"Enter a new hex code for {config_name} ({color_description}) [Current: {current_value}]: ").strip()
        if is_valid_hex(new_value):
            return new_value
        print("Invalid hex code. Please enter a valid hex color (e.g., #AABBCC).")

def update_configurations(customer_name, config_file="ui-configs.json"):
    """Main function to load and update configurations for a given customer."""
    # Create the customer-specific API URL
    api_url = get_api_url(customer_name)
    print(f"Using API URL: {api_url}")

    # Load and adjust the configurations file
    configs = load_configurations(config_file, customer_name)
    for config in configs:
        config_name = config["config_name"]
        current_value = config["config_value"]

        # If config requires user input, ask for a new color
        if config_name in UI_CONFIGS_TO_PROMPT:
            config["config_value"] = prompt_for_color(config_name, current_value, UI_CONFIGS_TO_PROMPT[config_name])

        print(f"Setting {config_name} to {config['config_value']}...")
        response = post_configuration(config, api_url)

        if response.ok:
            print(f"Success (POST): {config_name}")
        else:
            try:
                resp_json = response.json()
            except ValueError:
                resp_json = {}

            if response.status_code == 409 or (resp_json.get("code") == 409 and "already exists" in resp_json.get("message", "").lower()):
                print(f"Conflict for {config_name}. Attempting update via PUT...")
                put_response = put_configuration(config, api_url)
                if put_response.ok:
                    print(f"Success (PUT): {config_name}")
                else:
                    print(f"Failed to update {config_name} via PUT. Status: {put_response.status_code}, Response: {put_response.text}")
            else:
                print(f"Failed to set {config_name}. Status: {response.status_code}, Response: {response.text}")

# Only run if this script is executed directly
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python config_updater.py <customer_name>")
        sys.exit(1)
    customer_name = sys.argv[1]
    update_configurations(customer_name)
