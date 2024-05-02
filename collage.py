from PIL import Image
import os 

def collage(rows, cells, images_path):
    # List of lists of images
    images = [[os.path.join(images_path, f'{i}_{j}.jpg') for j in range(1, cells[i]+1)] for i in range(1, rows+1)]

    # Determine the size of the collage
    collage_height = len(images) * 200
    collage_width = max(len(row) for row in images) * 200

    # Create a new image for the collage
    collage = Image.new('RGB', (collage_width, collage_height), 'white')

    # Paste the images into the collage
    y = 0
    for row in images:
        x = 0
        img_width = collage_width // len(row)
        resized_imgs = [Image.open(i).resize((img_width, 200)) for i in row]
        for img in resized_imgs:
            collage.paste(img, (x, y))
            x += img_width
        y += 200

    # Save the collage
    meme_path = 'static/latest.jpg'
    collage.save(meme_path)