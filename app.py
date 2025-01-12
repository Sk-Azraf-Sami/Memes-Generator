from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PIL import Image
from addText import add_text
from padding import add_padding
from enhancement import histogram_equalization
from bgRemove import remove_background
from addCredit import add_credit
from gausBlur import gaussian_blur
from blackWhite import convert_to_black_and_white
import re
from collage import collage


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.config['COLLAGE_FOLDER'] = 'uploads'


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

        # If the file is not a jpg or jpeg, convert it to jpg
        if extension.lower() not in ['.jpg', '.jpeg']:
            img = Image.open(file_path).convert('RGB')
            new_filename = 'latest.jpg'
            new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            img.save(new_file_path, 'JPEG')
        elif extension.lower() == '.jpeg':
            # If the file is a jpeg, rename it to jpg
            img = Image.open(file_path)
            new_filename = 'latest.jpg'
            new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            img.save(new_file_path, 'JPEG')
        
        # Redirect to the meme-tools route
        return redirect(url_for('memegene'))
### Home page 
@app.route('/')
def index():
    return render_template('index.html')

### tool page 
@app.route('/meme-tools')
def memegene():
    return render_template('meme-tools.html')


#### add text
@app.route('/addtext', methods=['POST'])
def handle_add_text():
    top_text = request.form.get('top_text')
    font_size = int(request.form.get('font_size'))
    text_color = request.form.get('text_color')
    text_position = request.form.get('text_position')
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'latest.jpg')

    text_color = text_color[1:]
    text_color = tuple(int(text_color[i:i+2], 16) for i in (0, 2, 4))

    meme_path = add_text(top_text, font_size, text_color, text_position, image_path)

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
def handle_enhance_image():
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'latest.jpg')
    histogram_equalization(image_path)
    return jsonify({'status': 'success'})

@app.route('/bg_remove', methods=['POST'])
def handle_bg_remove():
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'latest.jpg')
    remove_background(image_path)
    return jsonify({'status': 'success'})

@app.route('/add_credit', methods=['POST'])
def handle_add_credit():
    credit_text = request.form.get('credit_text')
    font_size = int(request.form.get('font_size'))
    opacity = float(request.form.get('opacity'))
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'latest.jpg')
    boldness = int(request.form.get('boldness'))
    text_color = request.form.get('text_color')
    
     # Remove the '#' from the start of the color value
    text_color = text_color[1:]

    # Convert the color from hex to BGR
    text_color = tuple(int(text_color[i:i+2], 16) for i in (0, 2, 4))
    
    meme_path = add_credit(credit_text, font_size, opacity, text_color, boldness, image_path)

    return jsonify({'file_path': meme_path})

@app.route('/gausBlur', methods=['POST'])
def handle_gaussian_blur():
    kernel_size = int(request.form['kernel_size'])
    sigma = float(request.form['sigma'])
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'latest.jpg')

    meme_path = gaussian_blur(kernel_size, sigma, image_path)

    return jsonify({'file_path': meme_path})

@app.route('/black_white', methods=['POST'])
def handle_black_white():
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'latest.jpg')
    convert_to_black_and_white(image_path)
    return jsonify({'status': 'success'})


@app.route('/grid', methods=['POST'])
def handle_grid():
    # Get the number of rows from the form
    rows = int(request.form['rows'])
    
    #print(rows)

    # Prepare the cells parameter
    cells = [0] * rows

    # Iterate over each file in the form
    for file_key in request.files:
        # Get the file
        file = request.files[file_key]

        # If the user does not select a file, the browser submits an empty file
        if file.filename == '':
            continue

        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)

        # Convert the image to jpg if it's not already
        if not filename.lower().endswith('.jpg'):
            im = Image.open(file)
            filename = os.path.splitext(filename)[0] + '.jpg'
            im.convert('RGB').save(os.path.join(app.config['COLLAGE_FOLDER'], filename), 'JPEG')
        else:
            # Save the file to the uploads folder
            file.save(os.path.join(app.config['COLLAGE_FOLDER'], filename))
        
        
        # Print the file_key for debugging
        #print(f'file_key: {file_key}')
        # Rename the file to match the row and cell number
        match = re.match(r'image(\d+)_(\d+)', file_key)
        if match:
            row_number = int(match.group(1))
            cell_number = int(match.group(2))
            #print("row number:", row_number)
            #print("cell_number:", cell_number)
            new_filename = f'{row_number}_{cell_number}.jpg'
            os.rename(os.path.join(app.config['COLLAGE_FOLDER'], filename), os.path.join(app.config['COLLAGE_FOLDER'], new_filename))

            # Update the cells parameter
            cells[row_number - 1] = max(cells[row_number - 1], cell_number)

    
    #print('after calling function ==>', rows)
    # Call the collage function
    collage_path = collage(rows, cells, app.config['COLLAGE_FOLDER'])
    #print('rows number==>', rows)

    # Return a JSON response
    return jsonify({'status': 'success', 'file_path': collage_path})
    
    
if __name__ == '__main__':
    app.run(debug=True)