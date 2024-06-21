from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from werkzeug.utils import secure_filename
import cv2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def histogram_equalization(image_path):
    # Open the image with PIL
    img = Image.open(image_path).convert('RGB')
    
    # Convert the PIL image to a NumPy array
    img = np.array(img)

    if len(img.shape) == 2:  # Grayscale image
        img_h, img_w = img.shape
        histogram = np.histogram(img.flatten(), bins=256, range=[0,256])[0]

        pdf = histogram / (img_h * img_w)
        cdf = np.zeros(256)
        temp = 0
        for i in range(256):
            temp += pdf[i]
            cdf[i] = temp

        cdf *= 255

        output = np.zeros((img_h, img_w))
        for i in range(img_h):
            for j in range(img_w):
                intensity = img[i, j]
                output[i, j] = np.round(cdf[intensity])

        output = output.astype(np.uint8)

    else:  # Color image
        # Convert to YCrCb color space
        img_ycrcb = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
        
        # Separate the channels
        y_channel, cr_channel, cb_channel = cv2.split(img_ycrcb)
        
        # Apply histogram equalization to the Y channel
        img_h, img_w = y_channel.shape
        histogram = np.histogram(y_channel.flatten(), bins=256, range=[0,256])[0]

        pdf = histogram / (img_h * img_w)
        cdf = np.zeros(256)
        temp = 0
        for i in range(256):
            temp += pdf[i]
            cdf[i] = temp

        cdf *= 255

        y_output = np.zeros((img_h, img_w))
        for i in range(img_h):
            for j in range(img_w):
                intensity = y_channel[i, j]
                y_output[i, j] = np.round(cdf[intensity])

        y_output = y_output.astype(np.uint8)
        
        # Merge the channels back
        img_ycrcb = cv2.merge((y_output, cr_channel, cb_channel))
        
        # Convert back to RGB color space
        output = cv2.cvtColor(img_ycrcb, cv2.COLOR_YCrCb2RGB)

    meme_path = 'static/latest.jpg'
    cv2.imwrite(meme_path, cv2.cvtColor(output, cv2.COLOR_RGB2BGR))

    return meme_path

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            meme_path = histogram_equalization(filepath)
            return render_template('result.html', meme_path=meme_path)
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)
