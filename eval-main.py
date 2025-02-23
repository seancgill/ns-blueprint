from create_domain import create_domain
from create_reseller import create_reseller
from create_image import process_images
from ui_configs import update_configurations
from connections import create_connection, create_second_connection, create_outbound_connection
from create_user import create_user
from create_device import create_device  # Import the new module
from create_training_domains import create_training_domains

if __name__ == "__main__":
    cust_id = input("Enter the host ID: ")
    domain = input("Enter the domain name: ")
    
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

    create_reseller(custID, reseller, description)
    image_url = input("Enter the image URL (or 'n' to skip): ")
    if image_url.lower() != "n":
        process_images(image_url, custID)
    update_configurations(custID)
    create_connection(custID)
    create_second_connection(custID)
    create_outbound_connection(custID)
    create_domain(custID, domain, custID, 'made via api', domain, 'US and Canada', '858', 'NSEval', '8582834172', '8582834172')
    
    # Loop to create multiple users and devices
    while True:
        print("\n=== Creating a new user ===")
        create_user(custID, domain)
        print("\n=== Creating device for the user ===")
        extension = input("Enter the extension for the device (same as user): ").strip()
        create_device(custID, domain, extension)
        continue_prompt = input("Would you like to create another user? (y/n): ").strip().lower()
        if continue_prompt != 'y':
            print("Done creating users and devices.")
            break

create_training_domains(custID)