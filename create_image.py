import os
import requests
import mimetypes
import traceback
from resize import resize_image_from_url  # Import the resize function from resize.py
from dotenv import load_dotenv
from requests.utils import quote  # For encoding filenames in URLs

# Load environment variables
load_dotenv()

# Retrieve the API token from .env
API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN is missing from the environment variables!")

def create_image(domain, filename, file_path):
    """Uploads an image via API (POST) and retries with PUT if it already exists."""
    
    url = f"https://{domain}.trynetsapiens.com/ns-api/v2/images/{quote(filename, safe='')}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    payload = {
        "reseller": "*",
        "domain": "*",
        "server": f"{domain}.trynetsapiens.com",
        "description": "viaAPI"
    }

    # Get the correct MIME type of the file
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    try:
        with open(file_path, "rb") as file:
            files = {"File": (filename, file, mime_type)}
            
            print(f"Making API call to: {url} (POST)")
            response = requests.post(url, headers=headers, data=payload, files=files)

            if response.status_code in [400, 409]:  # 409 (Conflict) indicates file already exists
                print(f"Image already exists, trying PUT request for {filename}")
                response = requests.put(url, headers=headers, data=payload, files=files)

            print(f"API response for {filename}: {response.status_code} - {response.text}")

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred while uploading {filename}: {traceback.format_exc()}")

def process_images(image_url, domain):
    """Resizes images and uploads them to the API."""
    output_directory = "image_files"

    # Resize image and store in output directory
    resize_image_from_url(image_url, output_directory)

    # Define image mappings
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

if __name__ == "__main__":
    domain = input("Enter the domain: ").strip()
    image_url = input("Enter the image URL: ").strip()
    
    if domain and image_url:
        process_images(image_url, domain)
    else:
        print("Both domain and image URL are required!")
