from create_domain import create_domain
from create_reseller import create_reseller
from create_image import process_images
from ui_configs import update_configurations
from connections import create_connection, create_second_connection, create_outbound_connection
from create_user import create_user
#from create_image_orig import process_images

if __name__ == "__main__":
    cust_id = input("Enter the host ID: ")
    
    custID = f"{cust_id}"
    reseller = f"{cust_id}_reseller"
    description = "Created via API app"
    dial_plan = cust_id
    dial_policy = "US and Canada"
    area_code = 858
    caller_id_name = f"{cust_id} CID"
    caller_id_number = 18005551234
    caller_id_number_emergency = 18005551234
    

    create_reseller(custID, reseller, description)
    #update_custID_user(custID)
    # Prompt user for image URL
    image_url = input("Enter the image URL (or 'n' to skip): ")
    if image_url.lower() != "n":
        process_images(image_url, custID)
    update_configurations(custID)
    create_connection(custID)
    create_second_connection(custID)
    #create_outbound_connection(custID)
    create_domain(custID, 'letsrev', custID , 'made via api', 'letsrev', 'US and Canada', '858', 'letsrev', '8582834172', '8582834172')
    #create_domain(custID, 'letsrev', description, dial_plan, dial_policy, area_code, caller_id_name, caller_id_number, caller_id_number_emergency)
    create_user(custID, 'letsrev', '1001', 'Michael', 'Cheatwood', 'michael.cheatwood@letsrev.com')
