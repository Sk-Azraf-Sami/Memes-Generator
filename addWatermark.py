from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def add_watermark(upload_folder):
    
    watermark_text = request.form['watermark_text']
    font_size = int(request.form['font_size'])
    opacity = float(request.form['opacity'])
    
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
            image = Image.open(file).convert("RGBA")  # Convert image to RGBA mode
        except:
            return 'Invalid Image'
    
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Load font
    font = ImageFont.truetype("arial.ttf", font_size)
    
    # Calculate watermark text size and position
    text_width, text_height = textsize(watermark_text, font=font)
    width, height = image.size
    x = width - text_width - 10
    y = height - text_height - 10
    
    # Set watermark text color and opacity
    fill_color = (255, 255, 255, int(255 * opacity))  # White color with adjusted opacity
    draw.text((x, y), watermark_text, fill=fill_color, font=font)
    
    # Save modified image with a new filename
    modified_filename = f"{os.path.splitext(filename)[0]}-watermark{os.path.splitext(filename)[1]}"
    image.save(os.path.join('static', modified_filename))
        
    return render_template('result.html', modified_filename=modified_filename)