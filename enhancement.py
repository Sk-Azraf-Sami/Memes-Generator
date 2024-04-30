from flask import Flask, render_template, request
from PIL import Image
import cv2
import numpy as np
from werkzeug.utils import secure_filename

def histogram_equalization(image_path):
    # Open the image with PIL
    img = Image.open(image_path)

    # Convert the PIL image to an OpenCV image (numpy array)
    img = np.array(img)
    
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
    
    meme_path = 'static/latest.jpg'
    cv2.imwrite(meme_path, output)

    return meme_path