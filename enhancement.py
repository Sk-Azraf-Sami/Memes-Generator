from flask import Flask, render_template, request
from PIL import Image
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import os 

def histogram_equalization(upload_folder):
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
            img = np.array(img)  # Convert PIL Image to NumPy array
        except:
            return 'Invalid Image'
    
    img_h, img_w = img.shape[:2]  # Get height and width of the image
    
    histogram = np.zeros(256)
    histogram = cv2.calcHist([img], [0], None, [256], [0, 256])

    pdf = histogram / (img_h * img_w)
    cdf = np.zeros(256)
    temp = 0
    for i in range(256):
        temp += pdf[i]
        cdf[i] = temp

    cdf *= 255

    output = np.zeros((img_h, img_w))
    for i in range(img_h):
        for j in range(img_w):
            intensity = img[i, j]
            output[i, j] = np.round(cdf[intensity])

    output = cv2.normalize(output, None, 0, 1, cv2.NORM_MINMAX)
    output = output * 255
    output = output.astype(np.uint8)

    output_histogram = np.zeros(256)
    output_histogram = cv2.calcHist([output], [0], None, [256], [0, 256])
    output_pdf = output_histogram / (img_h * img_w)

    output_cdf = np.zeros(256)
    temp = 0
    for i in range(256):
        temp += output_pdf[i]
        output_cdf[i] = temp

    output_cdf *= 255
    
    # Save modified image with a new filename
    modified_filename = f"{os.path.splitext(filename)[0]}-enhance{os.path.splitext(filename)[1]}"
    Image.fromarray(output).save(os.path.join('static', modified_filename))

    return render_template('result.html', modified_filename=modified_filename)
