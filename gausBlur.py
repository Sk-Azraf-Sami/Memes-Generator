import cv2
import numpy as np
import math
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from PIL import Image

def gaussian_blur(kernel_size, sigma, image_path):
    
    # Open the image with PIL
    img = Image.open(image_path)
    
    # Convert the PIL Image to a NumPy array
    img = np.array(img)
    
    # Check if the image is grayscale or color
    if len(img.shape) == 2:
        is_grayscale = True
    else:
        is_grayscale = False
    
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
            if is_grayscale:
                # Handle grayscale image
                temp = 0
                for i in range(max(-padding_x, -x), min(padding_x, output_image_h - x - 1) + 1):
                    for j in range(max(-padding_y, -y), min(padding_y, output_image_w - y - 1) + 1):
                        temp += img[x-i, y-j]*gaussian_kernel[i,j]
                gaussian_output[x,y] = temp
            else:
                # Handle color image
                for channel in range(3):
                    temp = 0
                    for i in range(max(-padding_x, -x), min(padding_x, output_image_h - x - 1) + 1):
                        for j in range(max(-padding_y, -y), min(padding_y, output_image_w - y - 1) + 1):
                            temp += img[x-i, y-j, channel]*gaussian_kernel[i,j]
                    gaussian_output[x,y,channel] = temp

    # Crop the image to its original size
    gaussian_output = gaussian_output[padding_x:-padding_x, padding_y:-padding_y]
    
    gaussian_output = gaussian_output.astype(np.uint8)

    meme_path = 'static/latest.jpg'
    cv2.imwrite(meme_path, gaussian_output)

    return meme_path