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

# Mapping of shorthand scope values to full names
SCOPE_MAPPING = {
    "su": "Super User",
    "res": "Reseller",
    "om": "Office Manager",
    "adv": "Advanced User"
}

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

YES_NO_CONFIGS = [
    "PORTAL_USERS_DIR_MATCH_FIRSTNAME",
    "PORTAL_THREE_WAY_CALL_DISCONNECT_OTHERS_ON_END"
]

NUMERIC_CONFIGS = {
    "PORTAL_USERS_SECURE_PASSWORD_MIN_LENGTH": 8,
    "PORTAL_USERS_SECURE_PASSWORD_MIN_CAPITAL_LETTER_COUNT": 1,
    "PORTAL_USERS_SECURE_PASSWORD_MIN_NUMBER_COUNT": 1,
    "PORTAL_USERS_MIN_PASSWORD_LENGTH": 4,
    "PORTAL_USERS_SECURE_PASSWORD_MIN_SPECIAL_CHAR_COUNT": 0
}

STRING_CONFIGS = [
    "PORTAL_LOGGED_IN_POWERED_BY"
]

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
    return f"https://{customer_name}.trynetsapiens.com/ns-api/v2/configurations"

def load_configurations(filename, customer_name):
    """Load configuration data from a JSON file and replace 'custID' with customer_name."""
    with open(filename, 'r') as file:
        configs = json.load(file)
    
    for config in configs:
        if isinstance(config.get("config_value"), str):
            config["config_value"] = config["config_value"].replace("custID", customer_name)
    return configs

def is_valid_hex(color):
    """Check if input is a valid hex color code."""
    return bool(re.fullmatch(r"^#([A-Fa-f0-9]{6})$", color))

def prompt_for_yes_no(config_name, current_value):
    """Prompt user for a yes/no value."""
    while True:
        new_value = input(f"Enter 'yes' or 'no' for {config_name} [Current: {current_value}]: ").strip().lower()
        if new_value in ["y", "yes"]:
            return "yes"
        elif new_value in ["n", "no"]:
            return "no"
        print("Invalid input. Please enter 'yes' or 'no'.")

def prompt_for_numeric(config_name, current_value, min_value=0, max_value=9):
    """Prompt user for a single digit numeric value."""
    while True:
        new_value = input(f"Enter a number between {min_value} and {max_value} for {config_name} [Current: {current_value}]: ").strip()
        if new_value.isdigit() and min_value <= int(new_value) <= max_value:
            return new_value
        print(f"Invalid input. Please enter a number between {min_value} and {max_value}.")

def prompt_for_string(config_name, current_value):
    """Prompt user for a string value."""
    return input(f"Enter a value for {config_name} [Current: {current_value}]: ").strip()

def send_configuration(config, api_url, scope=None):
    """Send the configuration to the API, considering scope if applicable."""
    payload = common_payload.copy()
    payload["config-name"] = config["config_name"]
    payload["config-value"] = config["config_value"]
    
    if scope:
        payload["user-scope"] = scope
    
    response = requests.post(api_url, headers=headers, json=payload)
    print(f"POST status code for {config['config_name']} (Scope: {scope if scope else 'Default'}): {response.status_code}")
    return response

def update_configurations(customer_name, config_file="ui-configs.json"):
    """Main function to load and update configurations for a given customer."""
    api_url = get_api_url(customer_name)
    print(f"Using API URL: {api_url}")

    configs = load_configurations(config_file, customer_name)
    for config in configs:
        config_name = config["config_name"]
        current_value = config["config_value"]
        
        if config_name in UI_CONFIGS_TO_PROMPT:
            config["config_value"] = prompt_for_color(config_name, current_value, UI_CONFIGS_TO_PROMPT[config_name])
        elif config_name in YES_NO_CONFIGS:
            config["config_value"] = prompt_for_yes_no(config_name, current_value)
        elif config_name in NUMERIC_CONFIGS:
            config["config_value"] = prompt_for_numeric(config_name, current_value)
        elif config_name in STRING_CONFIGS:
            config["config_value"] = prompt_for_string(config_name, current_value)
        
        scopes = config.get("scopes", [])
        
        if scopes:
            for scope in scopes:
                full_scope_name = SCOPE_MAPPING.get(scope, scope)
                send_configuration(config, api_url, full_scope_name)
        else:
            send_configuration(config, api_url)

# Only run if this script is executed directly
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ui_configs.py <customer_name>")
        sys.exit(1)
    customer_name = sys.argv[1]
    update_configurations(customer_name)