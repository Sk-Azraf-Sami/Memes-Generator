from PIL import Image
import os 

def collage(rows, cells, images_path):
    # List of lists of images
    images = [[os.path.join(images_path, f'{i}_{j}.jpg') for j in range(1, cells[i-1]+1)] for i in range(1, rows+1)]
    
    image_size_factor = 400

    # Determine the size of the collage
    collage_height = len(images) * image_size_factor
    collage_width = max(len(row) for row in images) * image_size_factor

    # Create a new image for the collage
    collage = Image.new('RGB', (collage_width, collage_height), 'white')

    # Paste the images into the collage
    y = 0
    for row in images:
        x = 0
        img_width = collage_width // len(row)
        resized_imgs = [Image.open(i).resize((img_width, image_size_factor)) for i in row]
        for img in resized_imgs:
            collage.paste(img, (x, y))
            x += img_width
        y += image_size_factor

    # Save the collage
    meme_path = 'static/latest.jpg'
    collage.save(meme_path)