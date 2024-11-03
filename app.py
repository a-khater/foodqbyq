from flask import Flask, render_template, request, redirect, url_for
import openai
import os

# Load the OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Create the upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

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

        # Generate a prompt for ChatGPT based on the uploaded image context
        prompt = chatgpt_analysis_prompt(filepath)
        
        # Get the ChatGPT response
        analysis_result = call_chatgpt_api(prompt)

        return render_template('index.html', filepath=filepath, result=analysis_result)

def chatgpt_analysis_prompt(filepath):
    prompt = (
        "Evaluate the uploaded image for quality control. Focus on clarity, color accuracy, sharpness, resolution, "
        "alignment, and any visible defects (e.g., scratches, blurs). Provide a brief summary of any issues or "
        "areas for improvement."
    )
    return prompt


def call_chatgpt_api(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI specialized in image analysis and interpretation."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error in analysis: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
