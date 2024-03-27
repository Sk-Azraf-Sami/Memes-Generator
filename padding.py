import cv2
import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

def add_padding(upload_folder):
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
            img = cv2.imread(os.path.join(upload_folder, filename))
        except:
            return 'Invalid Image'
    
    top_padding = int(request.form['top_padding'])
    bottom_padding = int(request.form['bottom_padding'])
    left_padding = int(request.form['left_padding'])
    right_padding = int(request.form['right_padding'])
    padding_color = tuple(map(int, request.form['padding_color'].split(',')))

    # Add padding to the image
    padded_img = cv2.copyMakeBorder(img, top_padding, bottom_padding, left_padding, right_padding, cv2.BORDER_CONSTANT, value=padding_color)

    # Save modified image with a new filename
    modified_filename = f"{os.path.splitext(filename)[0]}-padded{os.path.splitext(filename)[1]}"
    cv2.imwrite(os.path.join('static', modified_filename), padded_img)
        
    return render_template('result.html', modified_filename=modified_filename)
