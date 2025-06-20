import os
import requests
import mimetypes
import traceback
import json
from resize import resize_image_from_url
from PIL import Image  # Added for local resizing
from dotenv import load_dotenv
from requests.utils import quote
from logging_setup import setup_logging

logger = setup_logging()
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN is missing from the environment variables!")
print(f"Loaded API_TOKEN: {API_TOKEN}")
logger.info(f"Loaded API_TOKEN: {API_TOKEN}")

def create_image(custID, filename, file_path, api_url, reseller=None):
    url = f"{api_url}/ns-api/v2/images/{quote(filename, safe='')}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    reseller_value = reseller if reseller else "*"
    payload = {
        "reseller": reseller_value,
        "domain": "*",
        "server": "*",
        "description": "viaAPI"
    }
    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    try:
        with open(file_path, "rb") as file:
            files = {"File": (filename, file, mime_type)}
            print(f"Making API call to: {url} (POST)")
            logger.info(f"Making API call to: {url} (POST) for reseller: {reseller_value}")
            logger.debug(f"Headers: {json.dumps(headers, indent=2)}")
            logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
            response = requests.post(url, headers=headers, data=payload, files=files)
            if response.status_code in [400, 409]:
                print(f"Image already exists, trying PUT request for {filename}")
                logger.info(f"Image already exists, trying PUT request for {filename}")
                response = requests.put(url, headers=headers, data=payload, files=files)
            print(f"API response for {filename}: {response.status_code} - {response.text}")
            logger.info(f"API response for {filename}: {response.status_code}")
            logger.debug(f"Response text: {response.text}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        logger.error(f"File {file_path} not found")
    except Exception as e:
        print(f"An error occurred while uploading {filename}: {traceback.format_exc()}")
        logger.error(f"An error occurred while uploading {filename}: {traceback.format_exc()}")

def process_images(image_source, custID, api_url, reseller=None, local=False, exclude_filenames=None):
    output_directory = "image_files"
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

    if exclude_filenames is None:
        exclude_filenames = []

    if local:
        # Process local file
        print(f"Processing local image: {image_source} for reseller: {reseller}")
        logger.info(f"Processing local image: {image_source} for reseller: {reseller}")
        if not os.path.exists(image_source):
            print(f"Local image file {image_source} not found")
            logger.error(f"Local image file {image_source} not found")
            return False  # Indicate failure
        
        with Image.open(image_source) as original_image:
            if original_image.mode == "RGBA":
                print("Converting RGBA image to RGB")
                logger.info("Converting RGBA image to RGB")
                original_image = original_image.convert("RGB")
            sizes = [(192, 192), (512, 512), (250, 150)]
            for size in sizes:
                resized_image = original_image.resize(size)
                filename = f"{size[0]}x{size[1]}"
                output_path = os.path.join(output_directory, f"{filename}.jpg")
                resized_image.save(output_path)
                print(f"Resized image saved to {output_path}")
                logger.info(f"Resized image saved to {output_path}")
    else:
        # Process URL
        print(f"Resizing image from URL: {image_source}")
        logger.info(f"Resizing image from URL: {image_source}")
        resize_image_from_url(image_source, output_directory)

    all_files_exist = all(os.path.exists(os.path.join(output_directory, image_file)) for image_file in filename_mapping.values())
    if not all_files_exist:
        print(f"Error: Not all resized images were created for {reseller or 'system'}")
        logger.error(f"Error: Not all resized images were created for {reseller or 'system'}")
        return False  # Indicate failure

    for filename, image_file in filename_mapping.items():
        if filename in exclude_filenames:
            print(f"Skipping upload for {filename} as per exclusion list")
            logger.info(f"Skipping upload for {filename} as per exclusion list")
            continue
        file_path = os.path.join(output_directory, image_file)
        print(f"Uploading {filename} from {file_path}")
        logger.info(f"Uploading {filename} from {file_path}")
        create_image(custID, filename, file_path, api_url, reseller)
    
    return True  # Indicate success

if __name__ == "__main__":
    print("Starting image processing script")
    logger.info("Starting image processing script")
    custID = input("Enter the host ID (e.g., sgdemo): ").strip()
    api_url = input("Enter the full API URL (e.g., https://api.example.ucaas.tech): ").strip()
    logger.info(f"Host ID entered: {custID}")
    logger.info(f"API URL entered: {api_url}")
    
    if not custID:
        print("Host ID is required!")
        logger.error("Host ID is required")
    else:
        while True:
            image_url = input("Enter the image URL (or local path if prefixed with 'file://', or press Enter to exit): ").strip()
            logger.info(f"Image source entered: {image_url}")
            
            if not image_url:  # Exit if user presses Enter without input
                print("No URL provided, exiting.")
                logger.info("No URL provided, exiting")
                break
            
            reseller_input = input("Enter the reseller value for image upload (or '*' for default): ").strip()
            logger.info(f"Reseller value entered for image upload: {reseller_input}")
            
            success = False
            if image_url.startswith("file://"):
                success = process_images(image_url[7:], custID, api_url, reseller=reseller_input, local=True)  # Strip 'file://' prefix
            else:
                success = process_images(image_url, custID, api_url, reseller=reseller_input)
            
            if success:
                print("Image processing completed successfully.")
                logger.info("Image processing completed successfully")
                break  # Exit loop on success
            else:
                print("Failed to process the image. Please try another URL.")
                logger.info("Prompting for another URL due to failure")

    print("Image processing script completed")
    logger.info("Image processing script completed")