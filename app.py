from flask import Flask, render_template
from addText import generate_meme
from enhancement import histogram_equalization
from bgRemove import remove_background
from addWatermark import add_watermark

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

# Route for background remover 
@app.route('/background_remover')
def backgroundRemove():
    # Perform actions for enhancement
    return render_template('bgRemove.html')

# Route for add watermark
@app.route('/add_watermark')
def addWatermark():
    # Perform actions for enhancement
    return render_template('addWatermark.html')


@app.route('/generate-meme', methods=['POST'])
def meme_generation():
    return generate_meme(app.config['UPLOAD_FOLDER'])

@app.route('/enhance', methods=['POST'])
def enhance_image():
    return histogram_equalization(app.config['UPLOAD_FOLDER'])

@app.route('/bg-remove', methods=['POST'])
def bgRemove():
    return remove_background(app.config['UPLOAD_FOLDER'])

@app.route('/add-watermark', methods=['POST'])
def addwatermark():
    return add_watermark(app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':
    app.run(debug=True)