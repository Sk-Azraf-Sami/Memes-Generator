import cv2
import numpy as np
import math
from PIL import Image

def gaussian_blur(kernel_size, sigma, image_path):
    # Open the image with PIL and convert to a NumPy array
    img = np.array(Image.open(image_path))
    
    # Determine if the image is grayscale or color
    is_grayscale = True if len(img.shape) == 2 else False
    
    # Generate Gaussian kernel
    def gaussian(k_size, sigma):
        offset = k_size // 2
        kernel = np.zeros((k_size, k_size))
        for x in range(-offset, offset + 1):
            for y in range(-offset, offset + 1):
                value = math.exp(-(x**2 + y**2) / (2 * sigma**2))
                kernel[x + offset, y + offset] = value
        kernel /= 2 * np.pi * sigma**2
        kernel /= kernel.sum()
        return kernel
    
    gaussian_kernel = gaussian(kernel_size, sigma)
    
    # Apply Gaussian blur using OpenCV if the image is not grayscale
    # OpenCV handles both grayscale and color images correctly
    if not is_grayscale:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV
    blurred_img = cv2.filter2D(img, -1, gaussian_kernel)
    if not is_grayscale:
        blurred_img = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2RGB)  # Convert back to RGB
    
    # Save the blurred image
    meme_path = 'static/latest.jpg'
    Image.fromarray(blurred_img).save(meme_path)
    
    return meme_path