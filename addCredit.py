from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def add_credit(credit_text, font_size, opacity, image_path):
    
    
    image = Image.open(image_path)
    
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Load font
    font = ImageFont.truetype("arial.ttf", font_size)
    
    # Calculate watermark text size and position
    text_width, text_height = textsize(credit_text, font=font)
    width, height = image.size
    x = width - text_width - 10
    y = height - text_height - 10
    
    # Set watermark text color and opacity
    fill_color = (255, 255, 255, int(255 * opacity))  # White color with adjusted opacity
    draw.text((x, y), credit_text, fill=fill_color, font=font)
    
    meme_path = 'static/latest.jpg'
    image.save(meme_path)

    return meme_path