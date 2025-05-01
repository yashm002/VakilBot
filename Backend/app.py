from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import pytesseract
from PIL import Image
import os
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
from flask_cors import CORS
import re

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Flask config
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load model
model_path = r"C:\Users\HP\OneDrive\Desktop\Mini_Project\Vakilbot\Fine tuned LLM model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# Clean extra spacing from OCR
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# OCR from PDF/Image
def extract_text_from_file(file_path):
    text = ""
    poppler_path = r"C:\Users\HP\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".pdf":
            images = convert_from_path(file_path, poppler_path=poppler_path)
            for img in images:
                text += pytesseract.image_to_string(img)
        else:
            # Handle single image or multi-frame TIFF
            with Image.open(file_path) as img:
                frames = []
                try:
                    while True:
                        frames.append(img.copy())
                        img.seek(img.tell() + 1)
                except EOFError:
                    pass

                for frame in frames:
                    text += pytesseract.image_to_string(frame)
    except Exception as e:
        print(f"[OCR ERROR] {e}")
        text = ""

    return text


@app.route('/summarize-text', methods=['POST'])
def summarize_text():
    try:
        data = request.get_json()
        user_text = data.get("text", "")

        if not user_text.strip():
            return jsonify({"error": "No input text provided."}), 400

        cleaned_text = clean_text(user_text)

        inputs = tokenizer.encode(cleaned_text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(
            inputs,
            max_length=768,
            min_length=300,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True,
            no_repeat_ngram_size=3
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        if not summary.endswith(('.', '?', '!')):
            summary = summary.rsplit('.', 1)[0] + '.'

        return jsonify({"summary": summary})
    
    except Exception as e:
        print("[ERROR]", e)
        return jsonify({"error": "Something went wrong processing the text."}), 500


# Upload endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Extract & clean text
    extracted_text = extract_text_from_file(filepath)
    cleaned_text = clean_text(extracted_text)

    # LLM Summarization
    inputs = tokenizer.encode(cleaned_text, return_tensors="pt", max_length=1024, truncation=True)

    summary_ids = model.generate(
        inputs,
        max_length=768,
        min_length=300,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True,
        no_repeat_ngram_size=3
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # If it ends mid-sentence, clean it
    if not summary.endswith(('.', '?', '!')):
        summary = summary.rsplit('.', 1)[0] + '.'

    return jsonify({"summary": summary})  # ✅ return to frontend

# Run app
if __name__ == '__main__':
    app.run(debug=True)
