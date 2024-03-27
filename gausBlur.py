import cv2
import numpy as np
import math
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

def gaussian_blur(upload_folder):
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
    
    def gaussian(k_size, sigma):
        gas_kernel = np.zeros((k_size, k_size))
        norm = 0
        gas_padding = (gas_kernel.shape[0] - 1) // 2
        for x in range(-gas_padding, gas_padding+1):
            for y in range(-gas_padding, gas_padding+1):
                c = 1/(2*3.1416*(sigma ** 2))
                gas_kernel[x+gas_padding, y+gas_padding] = c * math.exp(-(x ** 2 + y ** 2)/(2 * sigma ** 2))
                norm += gas_kernel[x+gas_padding, y+gas_padding]
        return gas_kernel/norm

    image_h = img.shape[0]
    image_w = img.shape[1]
    
    kernel_size = int(request.form['kernel_size'])
    sigma = float(request.form['sigma'])

    gaussian_kernel = gaussian(kernel_size, sigma)
    padding_x = kernel_size // 2
    padding_y = kernel_size // 2

    # Pad the image symmetrically
    img = cv2.copyMakeBorder(img, padding_y, padding_y, padding_x, padding_x, cv2.BORDER_REFLECT)

    output_image_h = image_h + kernel_size - 1
    output_image_w = image_w + kernel_size - 1

    gaussian_output = np.zeros((output_image_h,output_image_w, 3))
    for x in range(padding_x, output_image_h-padding_x):
        for y in range(padding_y, output_image_w-padding_y):
            for channel in range(3):
                temp = 0
                for i in range(-padding_x, padding_x+1):
                    for j in range(-padding_y, padding_y+1):
                        temp += img[x-i, y-j, channel]*gaussian_kernel[i+padding_x,j+padding_y]
                gaussian_output[x,y,channel] = temp
    gaussian_output = cv2.normalize(gaussian_output, None, 0, 255, cv2.NORM_MINMAX)

    # Crop the image to its original size
    gaussian_output = gaussian_output[padding_x:-padding_x, padding_y:-padding_y]

    # Save modified image with a new filename
    modified_filename = f"{os.path.splitext(filename)[0]}-gaussianblur{os.path.splitext(filename)[1]}"
    cv2.imwrite(os.path.join('static', modified_filename), gaussian_output.astype(np.uint8))
        
    return render_template('result.html', modified_filename=modified_filename)