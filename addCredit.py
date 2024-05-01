from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def add_credit(credit_text, font_size, opacity, text_color, boldness, image_path):
    
    # default boldness
    boldness = 0
    
    image = Image.open(image_path)
    
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Load font
    font = ImageFont.truetype("arial.ttf", font_size)
    
    # Calculate watermark text size and position
    text_width, text_height = textsize(credit_text, font=font)
    width, height = image.size

    # Adjust font size if text is too wide
    while text_width + 20 > width:
        font_size -= 1
        font = ImageFont.truetype("arial.ttf", font_size)
        text_width, text_height = textsize(credit_text, font=font)

    x = width - text_width - 10
    y = height - text_height - 10
    
    # Set watermark text color and opacity
    fill_color = (*text_color, int(255 * opacity))  # Use text_color with adjusted opacity

    # Draw text multiple times with slight offsets to mimic boldness
    for dx in range(-boldness, boldness+1):
        for dy in range(-boldness, boldness+1):
            draw.text((x+dx, y+dy), credit_text, fill=fill_color, font=font)
    
    meme_path = 'static/latest.jpg'
    image.save(meme_path)