from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from addText import generate_meme

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
        return jsonify(success=True, file_path=file_path), 200

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-meme', methods=['POST'])
def handle_generate_meme():
    top_text = request.form.get('top_text')
    bottom_text = request.form.get('bottom_text')
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'latest.jpg')

    meme_path = generate_meme(top_text, bottom_text, image_path)

    return jsonify({'file_path': meme_path})

if __name__ == '__main__':
    app.run(debug=True)
