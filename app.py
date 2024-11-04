
from flask import Flask, render_template, request, redirect, url_for
import openai
import base64
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_image(file_content):
    # Convert image content to base64
    encoded_image = base64.b64encode(file_content).decode()

    # Prepare the prompt with the base64 image included
    prompt = (
        "Analyze the following image provided as a base64-encoded string for quality control. "
        "Evaluate clarity, color accuracy, sharpness, resolution, alignment, and any visible defects. "
        "Summarize any quality issues or areas for improvement.\n\n"
        f"Image (base64): {encoded_image}"
    )

    # Call OpenAI's GPT-4 Turbo model with the prompt
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in image analysis and quality control."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the response content
    result_text = response['choices'][0]['message']['content']

    # Return the response as a dictionary for display
    return {
        "status": "Non-compliant" if "defect" in result_text.lower() else "Compliant",
        "summary": result_text,
        "full_report": "Full report provided by GPT-4 Turbo."
    }

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files.get('photo')
        if file and file.filename:
            # Read file in-memory
            file_content = file.read()
            
            # Call the analyze_image function with the file content
            results = analyze_image(file_content)
            
            return render_template('home.html', results=results)
    return render_template('home.html', results=None)

if __name__ == '__main__':
    app.run()
