from create_domain import create_domain
from create_reseller import create_reseller
from create_image import process_images
from ui_configs import update_configurations
from connections import create_connection, create_second_connection, create_outbound_connection
from create_user import create_user
from create_device import create_device  
from create_training_domains import create_training_domains
from logging_setup import setup_logging

# Initialize logger
logger = setup_logging()

if __name__ == "__main__":
    print("Starting NetSapiens API setup script")  # Keep for terminal
    logger.info("Starting NetSapiens API setup script")  # Log to file and terminal
    
    cust_id = input("Enter the host ID: ")
    domain = input("Enter the domain name: ")
    logger.info(f"Host ID entered: {cust_id}")
    logger.info(f"Domain name entered: {domain}")
    
    custID = f"{cust_id}"
    domain = f"{domain}"
    reseller = f"{cust_id}_reseller"
    description = "Created via API app"
    dial_plan = cust_id
    dial_policy = "US and Canada"
    area_code = 858
    caller_id_name = f"{cust_id} CID"
    caller_id_number = 18005551234
    caller_id_number_emergency = 18005551234

    print(f"Creating reseller: {reseller}")  # Keep for terminal
    logger.info(f"Creating reseller: {reseller}")
    create_reseller(custID, reseller, description)
    
    image_url = input("Enter the image URL (or 'n' to skip): ")
    if image_url.lower() != "n":
        print(f"Processing image URL: {image_url}")  # Keep for terminal
        logger.info(f"Processing image URL: {image_url}")
        process_images(image_url, custID)
    else:
        print("Skipping image processing")  # Keep for terminal
        logger.info("Skipping image processing")
    
    # Add option to skip update_configurations
    config_prompt = input("Would you like to update configurations? (y/n): ").strip().lower()
    if config_prompt == 'y':
        print("Updating configurations")  # Keep for terminal
        logger.info("Updating configurations")
        update_configurations(custID)
    else:
        print("Skipping configuration updates")  # Keep original print
        logger.info("Skipping configuration updates")
    
    print("Creating connections")  # Keep for terminal
    logger.info("Creating connections")
    create_connection(custID)
    create_second_connection(custID)
    create_outbound_connection(custID)
    
    print(f"Creating domain: {domain}")  # Keep for terminal
    logger.info(f"Creating domain: {domain}")
    create_domain(custID, domain, custID, 'made via api', domain, 'US and Canada', '858', 'NSEval', '8582834172', '8582834172')
    
    # Loop to create multiple users and devices
    while True:
        print("\n=== Creating a new user ===")  # Keep original print
        logger.info("=== Creating a new user ===")
        create_user(custID, domain)
        
        print("\n=== Creating device for the user ===")  # Keep original print
        logger.info("=== Creating device for the user ===")
        extension = input("Enter the extension for the device (same as user): ").strip()
        logger.info(f"Extension entered: {extension}")
        create_device(custID, domain, extension)
        
        continue_prompt = input("Would you like to create another user? (y/n): ").strip().lower()
        if continue_prompt != 'y':
            print("Done creating users and devices.")  # Keep original print
            logger.info("Done creating users and devices")
            break
        logger.info("Continuing to create another user")

    print("Creating training domains")  # Keep for terminal
    logger.info("Creating training domains")
    create_training_domains(custID)
    
    print("NetSapiens API setup script completed")  # Keep for terminal
    logger.info("NetSapiens API setup script completed")