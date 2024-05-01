from PIL import Image, ImageDraw, ImageFont
import os

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def add_text(top_text, bottom_text, font_size, opacity, boldness, text_color, image_path):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype("arial.ttf", font_size)

    top_text_width, top_text_height = textsize(top_text, font)
    bottom_text_width, bottom_text_height = textsize(bottom_text, font)

    # Adjust font size if text is too wide
    while max(top_text_width, bottom_text_width) > img.size[0]:
        font_size -= 1
        font = ImageFont.truetype("arial.ttf", font_size)
        top_text_width, top_text_height = textsize(top_text, font)
        bottom_text_width, bottom_text_height = textsize(bottom_text, font)

    top_text_x = (img.size[0] - top_text_width) / 2
    top_text_y = img.size[1] * 0.05
    bottom_text_x = (img.size[0] - bottom_text_width) / 2
    bottom_text_y = img.size[1] - bottom_text_height - (img.size[1] * 0.05)
    
    fill_color = (*text_color, int(255 * opacity))  # Use text_color with adjusted opacity

    # Draw text multiple times with slight offsets to mimic boldness
    for dx in range(-boldness, boldness+1):
        for dy in range(-boldness, boldness+1):
            draw.text((top_text_x+dx, top_text_y+dy), top_text, fill=fill_color, font=font)
            draw.text((bottom_text_x+dx, bottom_text_y+dy), bottom_text, fill=fill_color, font=font)
    
    meme_path = 'static/latest.jpg'
    img.save(meme_path)

    return meme_path