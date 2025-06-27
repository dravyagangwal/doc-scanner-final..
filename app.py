# app.py
from flask import Flask, render_template, request, jsonify
import os
import requests
import base64
from PIL import Image
import io
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['OPENROUTER_API_KEY'] = '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'
app.config['DEEPSEEK_R1_MODEL'] = 'deepseek/deepseek-r1-0528:free'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def image_to_base64(image_path):
    with Image.open(image_path) as img:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

def query_deepseek_r1(image_base64, prompt):
    headers = {
        "Authorization": f"Bearer {app.config['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": app.config['DEEPSEEK_R1_MODEL'],
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
                ]
            }
        ],
        "max_tokens": 2000
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"API Error: {response.text}")

def extract_aadhaar_data(image_path):
    # Convert image to base64
    image_base64 = image_to_base64(image_path)
    
    # Create detailed prompt
    prompt = """Extract all data from this Aadhaar card image and return in JSON format with the following structure:
    {
        "english": {
            "uid_number": "Aadhaar number (12 digits)",
            "name": "Full name in English",
            "gender": "Gender",
            "yob": "Year of Birth",
            "address": "Complete address in English",
            "qr_data": "QR code data if visible"
        },
        "hindi": {
            "uid_number": "आधार संख्या (12 अंक)",
            "name": "पूरा नाम हिंदी में",
            "gender": "लिंग",
            "yob": "जन्म वर्ष",
            "address": "पूरा पता हिंदी में",
            "qr_data": "QR कोड डेटा यदि दिखाई दे"
        }
    }
    
    Return ONLY the JSON object, no additional text or explanation."""
    
    # Query the LLM
    response = query_deepseek_r1(image_base64, prompt)
    
    try:
        # Extract JSON from response (sometimes LLMs add text around the JSON)
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        return json.loads(response[json_start:json_end])
    except json.JSONDecodeError:
        raise Exception("Failed to parse LLM response as JSON")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        try:
            extracted_data = extract_aadhaar_data(filename)
            return jsonify({
                'message': 'File processed successfully',
                'filename': file.filename,
                'fields': extracted_data
            })
        except Exception as e:
            return jsonify({'error': f'Data extraction failed: {str(e)}'}), 500
    

    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)