from io import BytesIO
from rembg import remove
from PIL import Image
import numpy as np

def remove_background(image_path):
    # Open the image
    with open(image_path, 'rb') as f:
        input_image = f.read()
    
    # Use rembg to remove the background
    output_image = remove(input_image)
    
    # Convert the output bytes to a PIL image
    img_with_transparency = Image.open(BytesIO(output_image))
    
    # Create a white background image of the same size
    white_background = Image.new("RGB", img_with_transparency.size, (255, 255, 255))
    
    # Paste the image onto the white background, using itself as the mask
    white_background.paste(img_with_transparency, mask=img_with_transparency.split()[3])  # Use the alpha channel as the mask
    
    # Save the result
    output_path = 'static/latest.jpg'
    white_background.save(output_path)
    
    return output_path