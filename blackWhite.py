from PIL import Image
import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

def convert_to_black_and_white(upload_folder):
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
            image = Image.open(file)
        except:
            return 'Invalid Image'
    
    # Convert the image to grayscale
    grayscale_image = image.convert('L')
    
    # Save modified image with a new filename
    modified_filename = f"{os.path.splitext(filename)[0]}-blackandwhite{os.path.splitext(filename)[1]}"
    grayscale_image.save(os.path.join('static', modified_filename))
        
    return render_template('result.html', modified_filename=modified_filename)
