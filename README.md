# 🆔 AI Aadhaar Data Extractor (Doc Scanner)

A web-based application built using **Flask**, **HTML/CSS/JS**, and **OpenRouter API** that allows users to upload an image of an Aadhaar card and extracts structured information in both **English** and **Hindi** using a powerful multimodal AI model.

---

## 🚀 Features

- 📤 Upload Aadhaar card images (JPEG, PNG, etc.)
- 📦 Drag-and-drop or browse upload options
- 🔍 AI-powered extraction of data fields using DeepSeek-R1 model
- 🌐 Displays extracted information in English and Hindi
- 🧠 Shows structured results + raw AI response
- 💾 Download options: CSV (English/Hindi), JSON (combined)
- 🎯 Supports real-time progress feedback and error handling
- 📱 Fully responsive UI with a clean and interactive design

---

## 🧠 How It Works

1. **Frontend (HTML/JS)**:
   - Image selection or drag-drop
   - Preview image
   - Submit to backend for processing
   - Shows structured and raw extracted data
   - CSV/JSON download options

2. **Backend (Flask - `app.py`)**:
   - Receives image via `/upload` endpoint
   - Converts image to base64
   - Sends prompt + image to DeepSeek-R1 model
   - Parses the returned AI-generated JSON
   - Returns it to frontend

3. **AI Prompting**:
   - Carefully designed prompt asks for Aadhaar card fields in both English and Hindi with a strict JSON-only output format.

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS (custom), JavaScript
- **Backend**: Python, Flask
- **AI Integration**: DeepSeek-R1 via OpenRouter API
- **Image Processing**: Pillow (PIL), base64
- **Others**: JSON parsing, drag & drop file support, Bootstrap-like UI

---

## 📝 Setup Instructions

### 🔧 Prerequisites

- Python 3.8+
- API Key from [OpenRouter.ai](https://openrouter.ai/)

### 📥 Installation

```bash
git clone https://github.com/yourusername/doc-scanner
cd doc-scanner
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 🔑 Add API Key

Open `app.py` and replace:
```python
app.config['OPENROUTER_API_KEY'] 
```
with your actual API key.

### ▶️ Run the App

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## 🚀 Deployment Options

### 🌐 Deploy to Render

1. Commit your code to GitHub
2. Go to [render.com](https://render.com)
3. Create a new Web Service
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python app.py`
6. Add environment variable `OPENROUTER_API_KEY`

### 🌍 Deploy with Railway

1. Login to [Railway](https://railway.app)
2. Link your GitHub repo
3. Add environment variable `OPENROUTER_API_KEY`
4. Deploy and you're live!

---

## 🗂 File Structure

```
├── app.py
├── index.html
├── requirements.txt
└── static/
    └── uploads/
```

---

## 🔐 Security & Privacy

- Images are temporarily stored and processed securely.
- No permanent data is stored.
- Keep your API key secure.

---

## 📌 Limitations

- Works only with image formats (not PDFs yet)
- Accuracy depends on image clarity
- QR decoding is LLM-based, not scanned

---

## 🇮🇳 Hindi Version Coming Soon...

README का हिंदी संस्करण जल्द ही उपलब्ध होगा।

---

## ✨ Author

by [Dravya Gangwal](https://github.com/dravyagangwal)
