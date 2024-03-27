import cv2
import numpy as np
from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename
import os


def remove_background(upload_folder, bg_color=(255, 255, 255)):
    
     # Check if the request contains the file part
    if 'image' not in request.files:
        return 'No file part'
    
    file = request.files['image']
    
    # If the user does not select a file, the browser submits an empty file without filename
    if file.filename == '':
        return 'No selected file'
    
    # If the file exists and is allowed
    if file:
        # Save the file to a secure location
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        try:
            img = Image.open(file)
            image = np.array(img)  # Convert PIL Image to NumPy array
        except:
            return 'Invalid Image'
    
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
        
    
    
    
    # Save modified image with a new filename
    modified_filename = f"{os.path.splitext(filename)[0]}-enhance{os.path.splitext(filename)[1]}"
    Image.fromarray(output).save(os.path.join('static', modified_filename))

    return render_template('result.html', modified_filename=modified_filename)
