import cv2
import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from PIL import Image

def add_padding(top_padding, bottom_padding, left_padding, right_padding, padding_color, image_path):
    # Open the image with PIL
    img = Image.open(image_path)

    # Convert the PIL image to an OpenCV image (numpy array)
    img = np.array(img)

    # Add padding to the image
    padded_img = cv2.copyMakeBorder(img, top_padding, bottom_padding, left_padding, right_padding, cv2.BORDER_CONSTANT, value=padding_color)

    # Convert the OpenCV image (numpy array) back to a PIL image
    padded_img = Image.fromarray(padded_img)

    meme_path = 'static/latest.jpg'
    padded_img.save(meme_path)

    return meme_path