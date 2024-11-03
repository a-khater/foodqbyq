from flask import Flask, render_template, request, redirect, url_for
import openai
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Set your OpenAI API key here
openai.api_key = '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'

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
    # Here you could include details about the image if needed
    # Currently, this is a generic prompt for demonstration
    prompt = (
        "Please analyze the uploaded image and provide insights or interpretations "
        "based on a general visual context. Note: This is a text-based analysis request."
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
