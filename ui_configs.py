import json
import requests
import os
import re
from dotenv import load_dotenv
import logging
from logging_setup import setup_logging

logger = setup_logging()
logger.setLevel(logging.DEBUG)  # Enable debug logging
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("Missing API token. Set NETSAPIENS_API_TOKEN as an environment variable.")
print(f"Loaded API_TOKEN: {API_TOKEN}")
logger.info(f"Loaded API_TOKEN: {API_TOKEN}")

SCOPE_MAPPING = {
    "su": "Super User",
    "res": "Reseller",
    "om": "Office Manager",
    "adv": "Advanced User",
    "cca": "Call Center Agent",
    "ccs": "Call Center Supervisor"
}

UI_CONFIG_PROMPT_COLOR_HEX = {
    "PORTAL_CSS_PRIMARY_1": "Dark Blue",
    "PORTAL_CSS_PRIMARY_2": "Green",
    "PORTAL_CSS_COLOR_MENU_BAR_PRIMARY_1": "Gray",
    "PORTAL_CSS_COLOR_MENU_BAR_PRIMARY_2": "Dark Blue",
    "PORTAL_WEBPHONE_PWA_BACKGROUND_COLOR": "Gray",
    "PORTAL_WEBPHONE_PWA_THEME_COLOR": "Green",
    "PORTAL_THEME_ACCENT": "Green",
    "PORTAL_THEME_PRIMARY": "Gray"
}

YES_NO_CONFIGS = [
    "PORTAL_USERS_DIR_MATCH_FIRSTNAME",
    "PORTAL_THREE_WAY_CALL_DISCONNECT_OTHERS_ON_END",
    "PORTAL_USERS_CALLERID_USE_DROPDOWN_DID_LIST"
]

NUMERIC_CONFIGS = {
    "PORTAL_USERS_SECURE_PASSWORD_MIN_LENGTH": 8,
    "PORTAL_USERS_SECURE_PASSWORD_MIN_CAPITAL_LETTER_COUNT": 1,
    "PORTAL_USERS_SECURE_PASSWORD_MIN_NUMBER_COUNT": 1,
    "PORTAL_USERS_MIN_PASSWORD_LENGTH": 4,
    "PORTAL_USERS_SECURE_PASSWORD_MIN_SPECIAL_CHAR_COUNT": 0
}

STRING_CONFIGS = [
    "PORTAL_LOGGED_IN_POWERED_BY",
    "PORTAL_PHONES_SNAPMOBILE_HOSTID"
]

common_payload = {
    "admin-ui-account-type": "*",
    "reseller": "*",
    "user": "*",
    "user-scope": "*",
    "core-server": "*",
    "domain": "*",
    "description": "Created via API"
}

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {API_TOKEN}",
    "content-type": "application/json"
}

def get_api_url(customer_name):
    return f"https://api.{customer_name}.ucaas.tech/ns-api/v2/configurations"

def load_configurations(filename, customer_name):
    with open(filename, 'r') as file:
        configs = json.load(file)
    for config in configs:
        if isinstance(config.get("config_value"), str):
            config["config_value"] = config["config_value"].replace("custID", customer_name)
    logger.info(f"Loaded configurations from {filename} with customer_name: {customer_name}")
    logger.debug(f"Configurations: {json.dumps(configs, indent=2)}")
    return configs

def prompt_for_color(config_name, current_value, default_value):
    while True:
        new_value = input(f"Enter a hex color code for {config_name} (e.g., #123abc) [Current: {current_value} | Default: {default_value}]: ").strip()
        if new_value == "":
            logger.info(f"Using default value '{default_value}' for {config_name}")
            return default_value
        if re.fullmatch(r"^#([A-Fa-f0-9]{6})$", new_value):
            logger.info(f"Accepted hex color '{new_value}' for {config_name}")
            return new_value
        print("Invalid hex color. Please enter a valid hex code (e.g., #123abc).")
        logger.warning(f"Invalid hex color input for {config_name}: {new_value}")

def prompt_for_yes_no(config_name, current_value):
    while True:
        new_value = input(f"Enter 'yes' or 'no' for {config_name} [Current: {current_value}]: ").strip().lower()
        if new_value in ["y", "yes"]:
            logger.info(f"Accepted 'yes' for {config_name}")
            return "yes"
        elif new_value in ["n", "no"]:
            logger.info(f"Accepted 'no' for {config_name}")
            return "no"
        print("Invalid input. Please enter 'yes' or 'no'.")
        logger.warning(f"Invalid yes/no input for {config_name}: {new_value}")

def prompt_for_numeric(config_name, current_value, min_value=0, max_value=9):
    while True:
        new_value = input(f"Enter a number between {min_value} and {max_value} for {config_name} [Current: {current_value}]: ").strip()
        if new_value.isdigit() and min_value <= int(new_value) <= max_value:
            logger.info(f"Accepted numeric value '{new_value}' for {config_name}")
            return new_value
        print(f"Invalid input. Please enter a number between {min_value} and {max_value}.")
        logger.warning(f"Invalid numeric input for {config_name}: {new_value}")

def prompt_for_string(config_name, current_value):
    new_value = input(f"Enter a value for {config_name} [Current: {current_value}]: ").strip()
    logger.info(f"Accepted string value '{new_value}' for {config_name}")
    return new_value

def send_configuration(config, api_url, scope=None):
    payload = common_payload.copy()
    payload["config-name"] = config["config_name"]
    payload["config-value"] = config["config_value"]
    
    if scope:
        payload["user-scope"] = scope
    
    if "reseller" in config:
        payload["reseller"] = config["reseller"]
    
    logger.info(f"Sending configuration {config['config_name']} (Scope: {scope if scope else 'Default'}, Reseller: {payload['reseller']}) to {api_url}")
    logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
    
    # First attempt with POST
    response = requests.post(api_url, headers=headers, json=payload)
    print(f"POST status code for {config['config_name']} (Scope: {scope if scope else 'Default'}, Reseller: {payload['reseller']}): {response.status_code}")
    logger.info(f"POST status code for {config['config_name']} (Scope: {scope if scope else 'Default'}, Reseller: {payload['reseller']}): {response.status_code}")
    logger.debug(f"Response text: {response.text}")
    
    # If 409 Conflict, attempt PUT
    if response.status_code == 409:
        logger.info(f"Conflict detected for {config['config_name']}, attempting PUT request")
        response = requests.put(api_url, headers=headers, json=payload)
        print(f"PUT status code for {config['config_name']} (Scope: {scope if scope else 'Default'}, Reseller: {payload['reseller']}): {response.status_code}")
        logger.info(f"PUT status code for {config['config_name']} (Scope: {scope if scope else 'Default'}, Reseller: {payload['reseller']}): {response.status_code}")
        logger.debug(f"PUT Response text: {response.text}")
    
    return response.status_code

def update_configurations(customer_name, config_file="ui-configs.json"):
    api_url = get_api_url(customer_name)
    print(f"Using API URL: {api_url}")
    logger.info(f"Using API URL: {api_url}")

    configs = load_configurations(config_file, customer_name)
    for config in configs:
        config_name = config["config_name"]
        current_value = config["config_value"]
        
        # Prompt only for system defaults (no reseller field)
        if "reseller" not in config:
            if config_name in UI_CONFIG_PROMPT_COLOR_HEX:
                config["config_value"] = prompt_for_color(config_name, current_value, UI_CONFIG_PROMPT_COLOR_HEX[config_name])
            elif config_name in YES_NO_CONFIGS:
                config["config_value"] = prompt_for_yes_no(config_name, current_value)
            elif config_name in NUMERIC_CONFIGS:
                config["config_value"] = prompt_for_numeric(config_name, current_value)
            elif config_name in STRING_CONFIGS:
                config["config_value"] = prompt_for_string(config_name, current_value)
        
        # Handle scopes (split comma-separated values)
        scopes = config.get("scopes", []) if "scopes" in config else config.get("scope", [])
        if isinstance(scopes, str):
            scopes = [scope.strip() for scope in scopes.split(",")]  # Split by comma and strip whitespace
        
        if scopes:
            for scope in scopes:
                full_scope_name = SCOPE_MAPPING.get(scope, scope)
                send_configuration(config, api_url, full_scope_name)
        else:
            send_configuration(config, api_url)

if __name__ == "__main__":
    import sys
    print("Starting UI configurations update script")
    logger.info("Starting UI configurations update script")
    
    if len(sys.argv) < 2:
        print("Usage: python ui_configs.py <customer_name>")
        logger.error("Missing customer_name argument. Usage: python ui_configs.py <customer_name>")
        sys.exit(1)
    
    customer_name = sys.argv[1]
    logger.info(f"Customer name provided: {customer_name}")
    update_configurations(customer_name)
    
    print("UI configurations update script completed")
    logger.info("UI configurations update script completed")