from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
from addText import add_text
from padding import add_padding
from enhancement import histogram_equalization

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(success=False, message='No file part'), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(success=False, message='No selected file'), 400

    if file:
        filename = secure_filename(file.filename)
        
        # Get the original extension
        _, extension = os.path.splitext(filename)
        
        # Rename the file to 'latest' with the original extension
        new_filename = 'latest' + extension
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(file_path)
        
        # Redirect to the meme-gene route
        return redirect(url_for('memegene'))

### Home page 
@app.route('/')
def index():
    return render_template('index.html')

### tool page 
@app.route('/meme-gene')
def memegene():
    return render_template('meme-gene.html')


#### add text
@app.route('/addtext', methods=['POST'])
def handle_add_text():
    top_text = request.form.get('top_text')
    bottom_text = request.form.get('bottom_text')
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'latest.jpg')

    meme_path = add_text(top_text, bottom_text, image_path)

    return jsonify({'file_path': meme_path})

@app.route('/padding', methods=['POST'])
def handle_padding():
    # Extract form data
    top_padding = int(request.form.get('top_padding'))
    bottom_padding = int(request.form.get('bottom_padding'))
    left_padding = int(request.form.get('left_padding'))
    right_padding = int(request.form.get('right_padding'))
    padding_color = request.form.get('padding_color')
    
     # Remove the '#' from the start of the color value
    padding_color = padding_color[1:]

    # Convert the color from hex to BGR
    padding_color = tuple(int(padding_color[i:i+2], 16) for i in (0, 2, 4))
    
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'latest.jpg')


    # Assuming you have a function to add padding to an image
    meme_path = add_padding(top_padding, bottom_padding, left_padding, right_padding, padding_color, image_path)

    # Return the path to the generated meme
    return jsonify({'file_path': meme_path})

@app.route('/enhance_image', methods=['POST'])
def enhance_image():
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'latest.jpg')
    histogram_equalization(image_path)
    return jsonify({'status': 'success'})
if __name__ == '__main__':
    app.run(debug=True)