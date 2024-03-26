from flask import Flask, render_template
from addText import generate_meme
from enhancement import histogram_equalization

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'


# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for adding text
@app.route('/add_text')
def add_text():
    # Perform actions for adding text
    return render_template('add_text.html')

# Route for padding
@app.route('/padding')
def padding():
    # Perform actions for padding
    return render_template('padding.html')

# Route for enhancement
@app.route('/enhancement')
def enhancement():
    # Perform actions for enhancement
    return render_template('enhancement.html')

# Route for collage
@app.route('/collage')
def collage():
    # Perform actions for collage
    return render_template('collage.html')


@app.route('/generate-meme', methods=['POST'])
def meme_generation():
    return generate_meme(app.config['UPLOAD_FOLDER'])

@app.route('/enhance', methods=['POST'])
def enhance_image():
    return histogram_equalization(app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':
    app.run(debug=True)