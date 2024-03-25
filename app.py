from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import random 
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

@app.route('/generate-meme', methods=['POST'])

def generate_meme():
    top_text = request.form['top_text']
    bottom_text = request.form['bottom_text']
    image_url = request.form['image_url']
    
    try:
        img = Image.open(requests.get(image_url, stream=True).raw)
    except:
        return 'Invalid Image Url'
    
    draw = ImageDraw.Draw(img)
    font_size = int(img.size[1]/5)
    font = ImageFont.truetype("arial.ttf", font_size)

    text_color = (255,255,255)
    outline_color = (0,0,0)
    outline_thickness = 2 

    top_text_width, top_text_height = textsize(top_text,font)
    bottom_text_width, bottom_text_height = textsize(bottom_text, font)
    
    top_text_x = (img.size[0] - top_text_width) / 2
    top_text_y = img.size[1] * 0.05
    bottom_text_x = (img.size[0] - bottom_text_width) / 2
    bottom_text_y = img.size[1] - bottom_text_height - (img.size[1] * 0.05)
    
    draw.text((top_text_x, top_text_y), top_text, fill=text_color, font=font, stroke_width=2)
    draw.text((bottom_text_x, bottom_text_y), bottom_text, fill=text_color, font=font, stroke_width=2)
    
    img.save('static/meme.png')
    
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)