import cv2
import numpy as np
from PIL import Image
import os

def remove_background(image_path):
    def custom_background_removal(img):
        np_img = np.array(img)
        Image.fromarray(np_img).save('static/step1_original.png')

        if len(np_img.shape) == 3 and np_img.shape[2] == 4:
            np_img = cv2.cvtColor(np_img, cv2.COLOR_RGBA2RGB)
        Image.fromarray(np_img).save('static/step2_rgb.png')

        mask = np.zeros(np_img.shape[:2], np.uint8)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)

        rect = (10, 10, np_img.shape[1] - 10, np_img.shape[0] - 10)
        cv2.grabCut(np_img, mask, rect, bgd_model, fgd_model, 15, cv2.GC_INIT_WITH_RECT)
        Image.fromarray(mask * 255).save('static/step3_mask.png')

        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        np_img = np_img * mask2[:, :, np.newaxis]
        Image.fromarray(np_img).save('static/step4_foreground.png')

        kernel = np.ones((3,3), np.uint8)
        np_img = cv2.morphologyEx(np_img, cv2.MORPH_OPEN, kernel, iterations=1)
        Image.fromarray(np_img).save('static/step5_morphology.png')

        alpha = np.where(mask2 == 0, 0, 255).astype(np.uint8)
        rgba = np.dstack((np_img, alpha))
        Image.fromarray(rgba).save('static/step6_rgba.png')

        return Image.fromarray(rgba)

    with open(image_path, 'rb') as f:
        img = Image.open(f)
        img.load()

    img_with_transparency = custom_background_removal(img)

    white_background = Image.new("RGB", img_with_transparency.size, (255, 255, 255))
    white_background.paste(img_with_transparency, mask=img_with_transparency.split()[3])
    white_background.save('static/step7_final.png')

    output_path = 'static/latest.jpg'
    white_background.save(output_path)

    return output_path

# Example usage
if __name__ == "__main__":
    image_path = 'latest.jpeg'
    output_path = remove_background(image_path)
    print(f"Output saved to {output_path}")