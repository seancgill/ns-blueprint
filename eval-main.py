from create_domain import create_domain
from create_reseller import create_reseller
from create_image import process_images
from ui_configs import update_configurations
from connections import create_connection, create_second_connection, create_outbound_connection
from routes import create_us_domestic_route
from create_user import create_user
from create_device import create_device  
from create_training_domains import create_training_domains
from logging_setup import setup_logging
import re

# Initialize logger
logger = setup_logging()

if __name__ == "__main__":
    print("Starting NetSapiens API setup script")
    logger.info("Starting NetSapiens API setup script")
    
    cust_id = input("Enter the host ID: ").strip()
    domain = input("Enter the domain name: ").strip()
    api_url = input("Enter the full API URL (e.g., https://api.example.ucaas.tech): ").strip()
    
    # Prepend https:// if the URL doesn't start with http:// or https://
    if not api_url.startswith(('http://', 'https://')):
        api_url = f"https://{api_url}"
        logger.info(f"Prepended https:// to API URL: {api_url}")
    
    # Validate api_url
    if not re.match(r"^https?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", api_url):
        print("Invalid API URL. Please enter a valid URL (e.g., https://api.example.ucaas.tech).")
        logger.error(f"Invalid API URL provided: {api_url}")
        exit(1)
    
    logger.info(f"API URL entered: {api_url}")
    logger.info(f"Host ID entered: {cust_id}")
    logger.info(f"Domain name entered: {domain}")
    
    custID = f"{cust_id}"
    domain = f"{domain}"
    reseller = f"{cust_id}_reseller"
    description = "Created via API app"
    dial_plan = cust_id
    dial_policy = "US and Canada"
    area_code = 615
    caller_id_name = f"{cust_id} CID"
    caller_id_number = 16156250119
    caller_id_number_emergency = 16156250119

    print(f"Creating reseller: {reseller}")
    logger.info(f"Creating reseller: {reseller}")
    create_reseller(custID, reseller, description, api_url)
    
    image_url = input("Enter the image URL (or 'n' to skip): ").strip()
    if image_url.lower() != "n":
        reseller_input = input("Enter the reseller value for image upload (or '*' for default): ").strip()
        logger.info(f"Reseller value entered for image upload: {reseller_input}")
        print(f"Processing image URL: {image_url}")
        logger.info(f"Processing image URL: {image_url}")
        process_images(image_url, custID, reseller=reseller_input, api_url=api_url)
    else:
        print("Skipping image processing")
        logger.info("Skipping image processing")
    
    config_prompt = input("Would you like to update configurations? (y/n): ").strip().lower()
    if config_prompt == 'y':
        print("Updating configurations")
        logger.info("Updating configurations")
        update_configurations(custID, api_url=api_url)
    else:
        print("Skipping configuration updates")
        logger.info("Skipping configuration updates")
    
    print("Creating connections")
    logger.info("Creating connections")
    create_connection(custID, api_url)
    create_second_connection(custID, api_url)
    create_outbound_connection(custID, api_url)
    print("Setting up US Domestic Route...")
    logger.info("Setting up US Domestic Route...")
    create_us_domestic_route(custID, api_url)

    print(f"Creating domain: {domain}")
    logger.info(f"Creating domain: {domain}")
    create_domain(custID, domain, custID, 'made via api', domain, 'US and Canada', '858', 'NSEval', '8582834172', '8582834172', api_url)
    
    while True:
        print("\n=== Creating a new user ===")
        logger.info("=== Creating a new user ===")
        create_user(custID, domain, api_url)
        
        print("\n=== Creating device for the user ===")
        logger.info("=== Creating device for the user ===")
        extension = input("Enter the extension for the device (same as user): ").strip()
        logger.info(f"Extension entered: {extension}")
        create_device(custID, domain, extension, api_url)
        
        continue_prompt = input("Would you like to create another user? (y/n): ").strip().lower()
        if continue_prompt != 'y':
            print("Done creating users and devices.")
            logger.info("Done creating users and devices")
            break
        logger.info("Continuing to create another user")

    print("Creating training domains")
    logger.info("Creating training domains")
    create_training_domains(custID, api_url)
    
    print("NetSapiens API setup script completed")
    logger.info("NetSapiens API setup script completed")