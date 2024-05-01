import cv2
import numpy as np
from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename
import os


def remove_background(image_path):
    
    bg_color=(255, 255, 255)
    
    # Open the image with PIL
    img = Image.open(image_path)

    # Convert the PIL image to an OpenCV image (numpy array)
    image = np.array(img)
    
    # Convert the image to grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)
    
    # Apply Otsu's thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create an all black mask
    mask = np.zeros_like(grayscale)
    
    # Fill in the contours
    cv2.drawContours(mask, contours, -1, 255, -1)
    
    # Create a copy of the image
    output = image.copy()
    
    # Set the background of the result to bg_color where the mask is black
    for c in range(3):
        output[:,:,c] = np.where(mask == 255, image[:,:,c], bg_color[c])
        
    
    meme_path = 'static/latest.jpg'
    cv2.imwrite(meme_path, output)

    return meme_path
