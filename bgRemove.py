import cv2
import numpy as np
from PIL import Image

def remove_background(image_path):
    def custom_background_removal(img):
        np_img = np.array(img)

        if len(np_img.shape) == 3 and np_img.shape[2] == 4:
            np_img = cv2.cvtColor(np_img, cv2.COLOR_RGBA2RGB)

        mask = np.zeros(np_img.shape[:2], np.uint8)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)

        # Improved initialization of the rectangle
        # Consider using a method to better approximate the foreground shape here
        rect = (10, 10, np_img.shape[1] - 10, np_img.shape[0] - 10)

        # Increase the number of iterations for more refinement
        cv2.grabCut(np_img, mask, rect, bgd_model, fgd_model, 15, cv2.GC_INIT_WITH_RECT)

        # Manual refinement of the mask can be done here if necessary

        # Apply the mask to get the foreground
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        np_img = np_img * mask2[:, :, np.newaxis]

        # Clean up the edges using morphological operations
        kernel = np.ones((3,3), np.uint8)
        np_img = cv2.morphologyEx(np_img, cv2.MORPH_OPEN, kernel, iterations=1)

        alpha = np.where(mask2 == 0, 0, 255).astype(np.uint8)
        rgba = np.dstack((np_img, alpha))

        return Image.fromarray(rgba)

    with open(image_path, 'rb') as f:
        img = Image.open(f)
        img.load()

    img_with_transparency = custom_background_removal(img)

    white_background = Image.new("RGB", img_with_transparency.size, (255, 255, 255))
    white_background.paste(img_with_transparency, mask=img_with_transparency.split()[3])

    output_path = 'static/latest.jpg'
    white_background.save(output_path)

    return output_path