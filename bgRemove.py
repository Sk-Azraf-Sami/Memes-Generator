import cv2
import numpy as np
from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename
import os


def remove_background(image_path):
    bg_color = (255, 255, 255)  # Background color to replace with
    
    # Open the image with PIL and convert it to RGB
    img = Image.open(image_path).convert('RGB')
    
    # Convert the PIL image to a NumPy array
    image = np.array(img)
    
    # Convert the image to grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)
    
    # Apply Otsu's thresholding to create a binary mask
    _, binary_mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Invert the mask if necessary. If the foreground is being removed instead of the background, invert the mask.
    binary_mask = cv2.bitwise_not(binary_mask)
    
    # Create a mask with three channels
    mask_3ch = cv2.cvtColor(binary_mask, cv2.COLOR_GRAY2RGB)
    
    # Apply the mask to the original image to isolate the foreground
    foreground = cv2.bitwise_and(image, mask_3ch)
    
    # Create an all-white background
    background = np.full_like(image, bg_color)
    
    # Combine the foreground with the background where the mask is not zero
    output = np.where(mask_3ch == bg_color, background, foreground)
    
    meme_path = 'static/latest.jpg'
    cv2.imwrite(meme_path, cv2.cvtColor(output, cv2.COLOR_RGB2BGR))
    
    return meme_path