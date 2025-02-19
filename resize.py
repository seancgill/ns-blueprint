import os
import requests
from PIL import Image
from io import BytesIO

def resize_image_from_url(image_url, output_directory):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Extract the filename from the URL
    image_filename = os.path.basename(image_url)

    # Download the image from the URL
    response = requests.get(image_url)
    if response.status_code == 200:
        # Open the image from the response content
        image_data = BytesIO(response.content)
        original_image = Image.open(image_data)
        
        # Convert RGBA image to RGB if necessary
        if original_image.mode == "RGBA":
            original_image = original_image.convert("RGB")
        
        # Resize the image to different dimensions
        sizes = [(192, 192), (512, 512), (250, 150)]
        for size in sizes:
            # Resize the image
            resized_image = original_image.resize(size)
            
            # Generate the filename based on dimensions
            filename = f"{size[0]}x{size[1]}"
            
            # Save the resized image with the generated filename
            output_path = os.path.join(output_directory, f"{filename}.jpg")
            resized_image.save(output_path)
            print(f"Resized image saved to {output_path}")
    else:
        print("Failed to download the image.")

if __name__ == "__main__":
    # Prompt user for image URL
    image_url = input("Enter the image URL: ")
    output_directory = 'image_files'
    resize_image_from_url(image_url, output_directory)
