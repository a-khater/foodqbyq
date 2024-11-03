from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Create the upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Home route with form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image upload and analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Simulate an AI analysis
        analysis_result = simulate_ai_analysis(filepath)
        
        return render_template('index.html', filepath=filepath, result=analysis_result)

def simulate_ai_analysis(image_path):
    # Simulate an analysis result - replace with real AI model call
    # Example: detect color properties of the image (as a placeholder for analysis)
    with Image.open(image_path) as img:
        colors = img.getcolors(256)
        main_color = max(colors, key=lambda x: x[0])[1]
    return f"Main color detected: RGB{main_color}"

if __name__ == '__main__':
    app.run(debug=True)
