from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PIL import Image, ImageDraw, ImageFont
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.config['COLLAGE_FOLDER'] = 'uploads'

def add_text(top_text, font_size, text_color, text_position, image_path):
    img = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", font_size)

    fill_color = (*text_color, 255)  # Use text_color with full opacity

    position = json.loads(text_position)
    text_x = position['x']
    text_y = position['y']
    text_width = position['width']
    text_height = position['height']

    draw.text((text_x, text_y), top_text, fill=fill_color, font=font)

    img = img.convert("RGB")
    meme_path = 'static/latest.jpg'
    img.save(meme_path)

    return meme_path