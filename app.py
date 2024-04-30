from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
from addText import add_text

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

if __name__ == '__main__':
    app.run(debug=True)