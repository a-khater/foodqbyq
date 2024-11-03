
import openai
import os
from flask import Flask, render_template, request, redirect, url_for

# Set up the OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No file selected")

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Generate a prompt for quality control analysis
        prompt = chatgpt_analysis_prompt(filepath)
        
        # Get the response using Completion API
        try:
            analysis_result = call_chatgpt_api(prompt)
            return render_template('index.html', filepath=filepath, result=analysis_result)
        except Exception as e:
            # Display any errors that occur during analysis
            return render_template('index.html', filepath=filepath, error=f"Error in analysis: {str(e)}")

def chatgpt_analysis_prompt(filepath):
    # Simple, effective prompt for quality control analysis
    prompt = (
        "Analyze the uploaded image for quality control purposes. "
        "Evaluate clarity, color accuracy, sharpness, resolution, alignment, "
        "and any visible defects. Summarize any quality issues or areas for improvement."
    )
    return prompt

def call_chatgpt_api(prompt):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Adjust if "gpt-4.0-mini" becomes available
            prompt=prompt,
            max_tokens=150,  # Control response length
            temperature=0.5   # Balanced for consistency
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error in analysis: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
    