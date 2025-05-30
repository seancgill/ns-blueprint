# NS-Blueprint UI Configurations Tool

The UI Configurations Tool (`ui_configs.py`) is a module of the **NS-Blueprint** framework, designed to streamline the setup of a customer’s NetSapiens UCaaS platform. This tool customizes UI and feature settings interactively during a live phone call with the customer. A Sales Engineer (SE) runs the script, which prompts them to ask the customer about specific feature preferences, inputting values based on their responses. UI configurations are one component of the broader NS-Blueprint customer setup process, which includes tasks like user provisioning, call flow configuration, and device management.

## Purpose

The `ui_configs.py` script enables SEs to tailor the NetSapiens platform’s UI and features in real-time as part of the NS-Blueprint setup. It:

- Loads a pre-built `ui-configs.json` file containing default configuration settings.
- Pauses for specific configurations to prompt the SE to ask the customer for input (e.g., “Do you want the dial-by-name directory to key off the first name or last name?”).
- Updates configuration values based on customer responses (e.g., setting `PORTAL_USERS_DIR_MATCH_FIRSTNAME` to `yes` or `no`).
- Sends configurations to the NetSapiens API, supporting scope-based (e.g., Super User, Call Center Agent) and reseller-specific settings.
- Handles API responses, including conflict resolution via PUT requests.

The `ui-configs.json` file is pre-configured with default values and does not require manual editing by the SE. The script uses these defaults as a baseline, prompting for customer input only when necessary to finalize specific settings.

## Prerequisites

- **Python 3.6+**: Ensure Python is installed.
- **Dependencies**: Install required Python packages:
  ```bash
  pip install requests python-dotenv
  ```
- **NetSapiens API Token**: Obtain a token for API access and set it as an environment variable (`NETSAPIENS_API_TOKEN`).
- **Configuration File**: A pre-built `ui-configs.json` file with default NetSapiens UI configurations (included in the NS-Blueprint repository).
- **Logging Setup**: A `logging_setup.py` module for logging (ensure it’s in the same directory or adjust the import).
- **NS-Blueprint Context**: This tool is part of the NS-Blueprint setup process. Coordinate with other setup components (e.g., user provisioning, call flows).

## Setup

1. **Clone the NS-Blueprint Repository**:

   ```bash
   git clone <ns-blueprint-repository-url>
   cd <ns-blueprint-directory>
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Create a `requirements.txt` with:

   ```
   requests
   python-dotenv
   ```

3. **Set Environment Variable**:
   Set the API token in a `.env` file or directly in your environment:

   ```bash
   echo "NETSAPIENS_API_TOKEN=your-api-token" > .env
   ```

   Or:

   ```bash
   export NETSAPIENS_API_TOKEN=your-api-token
   ```

4. **Verify Configuration File**:
   Ensure the pre-built `ui-configs.json` is in the project directory. This file contains default configuration objects, e.g.:

   ```json
   [
     {
       "config_name": "PORTAL_CSS_PRIMARY_1",
       "config_value": "#001a9b"
     },
     {
       "config_name": "PORTAL_USERS_DIR_MATCH_FIRSTNAME",
       "config_value": "yes"
     }
   ]
   ```

   The SE does not need to edit this file; the script uses its defaults and prompts for customer input as needed. Configurations may include optional `scope` (e.g., `su`, `cca`) or `reseller` fields.

5. **Logging Configuration**:
   Ensure `logging_setup.py` initializes the logger. If not using a custom setup, replace `from logging_setup import setup_logging` with:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   logger = logging.getLogger(__name__)
   ```

## Usage

As part of the NS-Blueprint customer setup, the SE runs the UI configurations tool during a live phone call to customize the NetSapiens platform:

```bash
python ui_configs.py [config_file]
```

- **config_file**: Optional path to the JSON configuration file (defaults to `ui-configs.json`).
- **Process**:
  1. The SE starts the script and enters the NetSapiens API URL.
  2. The script loads default configurations from the pre-built `ui-configs.json`.
  3. For specific configurations requiring customer input (e.g., UI colors, feature toggles), the script pauses and prompts the SE to ask the customer a question. The SE relays the customer’s response and enters the value.
  4. The script sends updated configurations to the NetSapiens API.
  5. Configurations not requiring input (e.g., reseller-specific or fixed settings) are sent using the default values from `ui-configs.json`.
- **Interactive Prompts**:
  - **Color Configs**: For UI elements (e.g., `PORTAL_CSS_PRIMARY_1`), the SE asks about color preferences and enters a hex code.
  - **Yes/No Configs**: For features like `PORTAL_USERS_DIR_MATCH_FIRSTNAME`, the SE asks, e.g., “Do you want the dial-by-name directory to key off the first name or last name?” and enters `yes` (first name) or `no` (last name).
  - **Numeric Configs**: For settings like `PORTAL_USERS_SECURE_PASSWORD_MIN_LENGTH`, the SE asks for a number within a range.
  - **String Configs**: For fields like `MOBILE_IOS_FEEDBACK_EMAIL`, the SE asks for text input.
- **Integration with NS-Blueprint**: This tool is run alongside other NS-Blueprint setup tasks (e.g., provisioning users, configuring call queues) to fully onboard the customer.

### Example

During a customer setup call, the SE runs:

```bash
python ui_configs.py ui-configs.json
```

**Prompts**:

```
Enter the full API URL (e.g., https://api.example.ucaas.tech): https://api.ucaas.tech
Enter a hex color code for PORTAL_CSS_PRIMARY_1 (e.g., #123abc) [Current: #001a9b | Default: Dark Blue]:
```

SE asks: “What primary color would you like for the portal’s UI?”
Customer: “A dark navy blue.”
SE enters: `#1a2b3c`

```
Enter 'yes' or 'no' for PORTAL_USERS_DIR_MATCH_FIRSTNAME [Current: yes]:
```

SE asks: “Do you want the dial-by-name directory to key off the first name or last name?”
Customer: “First name.”
SE enters: `yes`

```
Enter a number between 0 and 9 for PORTAL_USERS_SECURE_PASSWORD_MIN_LENGTH [Current: 8]:
```

SE asks: “What’s the minimum password length you want for users?”
Customer: “8 characters.”
SE enters: `8`

```
Enter a value for MOBILE_IOS_FEEDBACK_EMAIL [Current: ]:
```

SE asks: “What email should we use for iOS app feedback?”
Customer: “support@company.com.”
SE enters: `support@company.com`

**Output**:

```
POST status code for PORTAL_CSS_PRIMARY_1 (Scope: Default, Reseller: *): 201
POST status code for PORTAL_USERS_DIR_MATCH_FIRSTNAME (Scope: Default, Reseller: *): 201
...
UI configurations update script completed
```

### Configuration Types

The script prompts for customer input on specific configuration types, using defaults from `ui-configs.json` as a starting point:

- **Color Configs**: UI colors (e.g., `PORTAL_CSS_PRIMARY_1`). The SE asks for branding colors and enters hex codes.
- **Yes/No Configs**: Feature toggles (e.g., `PORTAL_USERS_DIR_MATCH_FIRSTNAME`). The SE asks yes/no questions about feature preferences.
- **Numeric Configs**: Numeric settings (e.g., `PORTAL_USERS_SECURE_PASSWORD_MIN_LENGTH`). The SE asks for numbers within valid ranges.
- **String Configs**: Text fields (e.g., `MOBILE_IOS_FEEDBACK_EMAIL`). The SE asks for text input.

Configs with a `reseller` field or those not requiring customer input are sent to the API using the default values in `ui-configs.json` without prompting.

### API Interaction

- **Endpoint**: POST requests are sent to `<api_url>/ns-api/v2/configurations`.
- **Payload**: Includes `config-name`, `config-value`, `user-scope`, `reseller`, and defaults from `common_payload`.
- **Conflict Handling**: If a POST returns a 409 (conflict), a PUT request updates the existing configuration.
- **Scopes**: Supports scope-specific settings (e.g., `su` for Super User, `cca` for Call Center Agent) using `SCOPE_MAPPING`.

## Logging

The script logs all actions for auditing and debugging within the NS-Blueprint process:

- Configuration loading from `ui-configs.json`.
- Customer-driven inputs and validation.
- API requests and responses (status codes, payloads, errors).
  Logs are configured via `logging_setup.py`. Use logs to track customer choices or troubleshoot issues.

## Customization

- **Add Features**: Update `ui-configs.json` with new default configurations to support additional NetSapiens features. No SE editing is required.
- **Modify Prompts**: Add configs to `UI_CONFIG_PROMPT_COLOR_HEX`, `YES_NO_CONFIGS`, `NUMERIC_CONFIGS`, or `STRING_CONFIGS` in `ui_configs.py` to customize customer questions.
- **Customer Name**: Pass a `customer_name` to `load_configurations` to replace `custID` in values (e.g., `PORTAL_FQDN` becomes `portal.customer.ucaas.tech`).
- **NS-Blueprint Integration**: Coordinate with other NS-Blueprint modules (e.g., user setup, call flow scripts) for a seamless customer onboarding experience.

## Troubleshooting

- **Invalid API Token**: Verify `NETSAPIENS_API_TOKEN` is set correctly.
- **API URL Errors**: Ensure the URL is valid and accessible.
- **JSON File Issues**: Confirm `ui-configs.json` is present and contains valid JSON. The file should not be edited by the SE.
- **Customer Input**: If the customer is unsure, the SE can use default values from `ui-configs.json` (e.g., press Enter for color configs).
- **NS-Blueprint Context**: Ensure this tool is run in the correct sequence with other setup tasks.
- **Logs**: Review logs for detailed error messages or to confirm customer selections.

## Example Configuration File

A sample `ui-configs.json` (pre-built, not edited by the SE):

```json
[
  {
    "config_name": "PORTAL_CSS_PRIMARY_1",
    "config_value": "#001a9b"
  },
  {
    "config_name": "PORTAL_USERS_DIR_MATCH_FIRSTNAME",
    "config_value": "yes"
  },
  {
    "config_name": "PORTAL_USERS_SECURE_PASSWORD_MIN_LENGTH",
    "config_value": "8"
  },
  {
    "config_name": "MOBILE_IOS_FEEDBACK_EMAIL",
    "config_value": ""
  }
]
```

## Best Practices for Sales Engineers

- **Preparation**: Review the NS-Blueprint setup steps and `ui-configs.json` to understand the default settings and customer-configurable features.
- **Customer Engagement**: Ask clear, concise questions (e.g., “Do you want the dial-by-name directory to use first names or last names?”) and explain features if needed.
- **Default Values**: Use defaults from `ui-configs.json` for non-critical settings if the customer is unsure (e.g., color defaults in `UI_CONFIG_PROMPT_COLOR_HEX`).
- **Coordination**: Align with other NS-Blueprint tasks to ensure a cohesive setup process.
- **Logging**: Save logs to document customer preferences for future reference or auditing.

## Contributing

Contributions to the NS-Blueprint UI Configurations Tool are welcome! Submit pull requests or open issues for bugs, new features, or improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
