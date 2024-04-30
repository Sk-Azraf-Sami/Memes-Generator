from PIL import Image, ImageDraw, ImageFont
import os

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def add_text(top_text, bottom_text, image_path):
    
    img = Image.open(image_path)
    
    draw = ImageDraw.Draw(img)
    font_size = int(img.size[1] / 5)
    font = ImageFont.truetype("arial.ttf", font_size)

    text_color = (255, 255, 255)
    outline_color = (0, 0, 0)
    outline_thickness = 2 

    top_text_width, top_text_height = textsize(top_text, font)
    bottom_text_width, bottom_text_height = textsize(bottom_text, font)
    
    top_text_x = (img.size[0] - top_text_width) / 2
    top_text_y = img.size[1] * 0.05
    bottom_text_x = (img.size[0] - bottom_text_width) / 2
    bottom_text_y = img.size[1] - bottom_text_height - (img.size[1] * 0.05)
    
    draw.text((top_text_x, top_text_y), top_text, fill=text_color, font=font, stroke_width=2)
    draw.text((bottom_text_x, bottom_text_y), bottom_text, fill=text_color, font=font, stroke_width=2)
    
    meme_path = 'static/latest.jpg'
    img.save(meme_path)

    return meme_path