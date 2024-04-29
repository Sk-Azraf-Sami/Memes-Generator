from PIL import Image
import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

def create_collage(upload_folder):
    # Check if the request contains the files part
    if 'images[]' not in request.files:
        return 'No file part'
    
    files = request.files.getlist('images[]')
    
    # If no files are selected
    if len(files) == 0:
        return 'No selected files'
    
    # Load all images and calculate total dimensions
    images = [Image.open(file) for file in files]
    total_width = sum(image.width for image in images)
    max_height = max(image.height for image in images)
    
    # Create a blank canvas for the collage
    collage = Image.new('RGB', (total_width, max_height))
    
    # Paste each image into the collage
    x_offset = 0
    for image in images:
        collage.paste(image, (x_offset, 0))
        x_offset += image.width
    
    # Save the collage with a new filename
    filename = 'collage.jpg'
    collage.save(os.path.join(upload_folder, filename))
    
    return render_template('result.html', modified_filename=filename)
