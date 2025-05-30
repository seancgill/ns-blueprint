import requests
import base64
import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThinQAPI:
    
    def __init__(self, username: str, api_token: str, account_id: str, base_url: str = "https://api.thinq.com"):
        self.base_url = base_url
        self.account_id = account_id
        self.auth = base64.b64encode(f"{username}:{api_token}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {self.auth}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*"
        }

    def create_inbound_routing_profile(self, profile_name: str, routes: List[Dict]) -> Optional[int]:
        """Create an inbound routing profile and return its ID."""
        if not profile_name or not routes:
            logger.error("Profile name and routes are required")
            return None
        url = f"{self.base_url}/account/{self.account_id}/staticinrouteprofile"
        payload = {
            "profile": {
                "name": profile_name,
                "inboundRoutes": routes
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            profile_id = response.json().get("profile", {}).get("id")
            logger.info(f"Created inbound routing profile '{profile_name}' with ID {profile_id}")
            return profile_id
        except requests.RequestException as e:
            logger.error(f"Failed to create inbound routing profile: {e}")
            return None

    def search_numbers(self, npa: str, quantity: int = 2) -> Optional[List[str]]:
        """Search for available numbers in the specified NPA."""
        if not npa or len(npa) != 3 or not npa.isdigit():
            logger.error("Invalid NPA: must be a 3-digit number")
            return None
        if quantity < 1:
            logger.error("Quantity must be positive")
            return None
        url = f"{self.base_url}/account/{self.account_id}/numbers/search"
        payload = {
            "search": {
                "npa": npa,
                "quantity": quantity,
                "cnam_enabled": True
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            numbers = [item["number"] for item in response.json().get("numbers", [])]
            if len(numbers) < quantity:
                logger.warning(f"Found only {len(numbers)} numbers instead of {quantity}")
            logger.info(f"Found {len(numbers)} numbers in NPA {npa}: {numbers}")
            return numbers
        except requests.RequestException as e:
            logger.error(f"Failed to search numbers: {e}")
            return None

    def purchase_numbers(self, numbers: List[str]) -> bool:
        """Purchase the specified numbers."""
        if not numbers:
            logger.error("No numbers provided for purchase")
            return False
        url = f"{self.base_url}/account/{self.account_id}/origination/did/order"
        payload = {
            "order": {
                "numbers": [
                    {
                        "number": number,
                        "cnam_enabled": True
                    } for number in numbers
                ],
                "group_id": None,
                "tax_exemption": False
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            order_id = response.json().get("order", {}).get("id")
            logger.info(f"Purchased numbers {numbers} with order ID {order_id}")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to purchase numbers: {e}")
            return False

    def assign_numbers_to_profile(self, dids: List[str], profile_id: int, enable_cnam: bool = True) -> bool:
        """Assign multiple numbers to an inbound routing profile."""
        if not dids or not profile_id:
            logger.error("DIDs and profile ID are required")
            return False
        url = f"{self.base_url}/account/{self.account_id}/origination/did/features/createbulk"
        payload = {
            "id": self.account_id,
            "order": {
                "searchParams": {
                    "dids": [int(did.lstrip("+")) for did in dids]
                },
                "featuresToEdit": {
                    "route_id": profile_id,
                    "cnam": enable_cnam
                }
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            order_id = response.json().get("order", {}).get("id")
            logger.info(f"Assigned numbers {dids} to profile ID {profile_id} with order ID {order_id}")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to assign numbers to profile: {e}")
            return False

    def create_outbound_trunk(self, trunk_name: str, profile_id: int, address: str, channel_limit: int = 30) -> Optional[int]:
        """Create an outbound trunk and return its ID."""
        if not trunk_name or not profile_id or not address:
            logger.error("Trunk name, profile ID, and address are required")
            return None
        url = f"{self.base_url}/outbound/trunks"
        payload = {
            "trunkTypeId": 1,
            "profileId": profile_id,
            "name": trunk_name,
            "channelLimit": channel_limit,
            "groupId": None,
            "address": address,
            "addressEnd": None,
            "prefix": None
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            trunk_id = response.json().get("data", {}).get("id")
            logger.info(f"Created outbound trunk '{trunk_name}' with ID {trunk_id}")
            return trunk_id
        except requests.RequestException as e:
            logger.error(f"Failed to create outbound trunk: {e}")
            return None

    def provision_thinq_numbers(self, npa: str, profile_name: str, routes: List[Dict], trunk_address: str, trunk_profile_id: int) -> bool:
        """Orchestrate the full provisioning process."""
        # Step 1: Create inbound routing profile
        profile_id = self.create_inbound_routing_profile(profile_name, routes)
        if not profile_id:
            return False

        # Step 2: Search for numbers
        numbers = self.search_numbers(npa)
        if not numbers:
            return False

        # Step 3: Purchase numbers
        if not self.purchase_numbers(numbers):
            return False

        # Step 4: Assign numbers to profile
        if not self.assign_numbers_to_profile(numbers, profile_id):
            return False

        # Step 5: Create outbound trunk
        trunk_id = self.create_outbound_trunk(profile_name, trunk_profile_id, trunk_address)
        if not trunk_id:
            return False

        logger.info("Provisioning completed successfully")
        return True

# Example usage
if __name__ == "__main__":
    thinq = ThinQAPI(
        username="sgill",
        api_token="555982ee38ec117ae5e3c85f6bf9b16a36b380b6",
        account_id="11151"
    )

    routes = [
        {
            "placeholder": "",
            "routePort": "5060",
            "routeToAddress": "170.9.240.78",
            "routeType": "IP"
        },
        {
            "placeholder": "200.115.222.100",
            "routePort": "5060",
            "routeToAddress": "64.181.209.113",
            "routeType": "IP"
        }
    ]

    success = thinq.provision_thinq_numbers(
        npa="310",
        profile_name="tigerconnect",
        routes=routes,
        trunk_address="170.9.240.78",
        trunk_profile_id=5936
    )

    if success:
        print("Provisioning completed successfully")
    else:
        print("Provisioning failed")