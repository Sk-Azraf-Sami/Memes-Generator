from PIL import Image
import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

def convert_to_black_and_white(image_path):
    image = Image.open(image_path)
    
    # Convert the image to grayscale
    grayscale_image = image.convert('L')
    
    meme_path = 'static/latest.jpg'
    grayscale_image.save(meme_path)

    return meme_path