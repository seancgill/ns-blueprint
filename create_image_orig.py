import os
import requests
from resize import resize_image_from_url  # Import the resize function from resize.py
import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

# Retrieve the API token
API_TOKEN = os.getenv("API_TOKEN")

def create_image(domain, filename, file_path):
    access_token = "nss_CrXxkB5RzajkNXO2hPN7ZwDgABlGQe5EroSBRufStr3XjVLg75a0dde5"
    url = f"https://{domain}.trynetsapiens.com/ns-api/v2/images/" + filename
    reseller = f"{domain}_reseller"

    headers = {
        "accept": "application/json",
        'Authorization': f'Bearer {API_TOKEN}'
    }

    payload = {
        "reseller": "*",  # Correctly format the reseller value
        #"reseller": reseller,  # Correctly format the reseller value
        "domain": "*",
        "server": f"{domain}.trynetsapiens.com",
        "description": "viaAPI"
    }

    try:
        with open(file_path, "rb") as file:
            files = {"File": (filename, file, "image/jpeg")}
            print(f"Making API call to: {url} (POST)")  # Print the exact URL API endpoint
            response = requests.post(url, headers=headers, data=payload, files=files)
            if response.status_code == 400 and "File already exists." in response.text:
                print(f"Image already exists, trying PUT request for {filename}")
                response = requests.put(url, headers=headers, data=payload, files=files)
            print(f"API response for {filename}: {response.text}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_images(image_url, domain):
    output_directory = 'image_files'

    # Call resize function to resize the image
    resize_image_from_url(image_url, output_directory)

    if True :
        # Map filenames to corresponding local image files
        filename_mapping = {
            "512PWA.png": "512x512.jpg",
            "192PWA.png": "192x192.jpg",
            "favicon.gif": "192x192.jpg",
            "video_main_top_left.png": "250x150.jpg",
            "video_login.png": "250x150.jpg",
            "portal_main_top_left.png": "250x150.jpg",
            "portal_landing.png": "250x150.jpg",
            "webphone_main_top_left.png": "250x150.jpg"
        }
        for filename, image_file in filename_mapping.items():
            file_path = os.path.join(output_directory, image_file)
            if os.path.exists(file_path):
                create_image(domain, filename, file_path)
            else:
                print(f"Resized image {image_file} not found.")
    else:
        print("Failed to obtain access token")

if __name__ == "__main__":
    domain = input("Enter the domain: ")
    image_url = input("Enter the image URL: ")
    process_images(image_url, domain)