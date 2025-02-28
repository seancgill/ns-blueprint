import os
import time
import requests
from PIL import Image
from io import BytesIO
from logging_setup import setup_logging

logger = setup_logging()

def resize_image_from_url(image_url, output_directory, max_retries=3):
    os.makedirs(output_directory, exist_ok=True)
    image_filename = os.path.basename(image_url)
    print(f"Downloading image from URL: {image_url}")
    logger.info(f"Downloading image from URL: {image_url}")
    logger.debug(f"Image filename extracted: {image_filename}")

    for attempt in range(max_retries):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                print("Image downloaded successfully")
                logger.info("Image downloaded successfully")
                image_data = BytesIO(response.content)
                original_image = Image.open(image_data)
                # Convert P or RGBA to RGB for JPEG compatibility
                if original_image.mode in ["P", "RGBA"]:
                    print(f"Converting {original_image.mode} image to RGB")
                    logger.info(f"Converting {original_image.mode} image to RGB")
                    original_image = original_image.convert("RGB")
                sizes = [(192, 192), (512, 512), (250, 150)]
                for size in sizes:
                    resized_image = original_image.resize(size)
                    filename = f"{size[0]}x{size[1]}"
                    output_path = os.path.join(output_directory, f"{filename}.jpg")
                    resized_image.save(output_path)
                    print(f"Resized image saved to {output_path}")
                    logger.info(f"Resized image saved to {output_path}")
                return  # Success, exit function
            elif response.status_code == 429:
                print(f"Rate limit hit (429), retrying {attempt + 1}/{max_retries}...")
                logger.warning(f"Rate limit hit (429), retrying {attempt + 1}/{max_retries}...")
                time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
            else:
                print(f"Failed to download the image. Status code: {response.status_code}")
                logger.error(f"Failed to download the image. Status code: {response.status_code}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")
            logger.error(f"Error downloading image: {e}")
            return
    print(f"Failed to download image after {max_retries} retries")
    logger.error(f"Failed to download image after {max_retries} retries")

if __name__ == "__main__":
    print("Starting image resize script")
    logger.info("Starting image resize script")
    image_url = input("Enter the image URL: ")
    logger.info(f"Image URL entered: {image_url}")
    output_directory = 'image_files'
    resize_image_from_url(image_url, output_directory)
    print("Image resize script completed")
    logger.info("Image resize script completed")