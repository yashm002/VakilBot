# Vakilbot
AI-Powered Legal Document Simplification

VakilBot is a legal document simplification tool designed to help users understand complex legal language by using a fine-tuned LLM model. It includes OCR capabilities to extract text from uploaded legal PDFs and provides simplified summaries.

# Download the Fine-Tuned Model

The fine-tuned model used for summarization is available here:

[Download Model from Google Drive](https://drive.google.com/drive/folders/1Z3pEWvfh1tmst6CuxnLlVuEcI9JTCazG?usp=sharing)

# Dataset Used for Fine-Tuning Model

This project uses the **Indian Court Judgements and Its Summaries** dataset from Hugging Face:

[Rishiai/indian-court-judgements-and-its-summaries](https://huggingface.co/datasets/rishiai/indian-court-judgements-and-its-summaries)

# Features

- Upload legal documents (PDF format)
- Extract text using Optical Character Recognition (OCR)
- Summarize complex legal language into simplified text
- Uses a fine-tuned transformer model for summarization
- Clean and user-friendly web interface

# Tech Stack

- Python
- Flask (or Streamlit, if applicable)
- Transformers (Hugging Face)
- PyTesseract for OCR
- GitHub for version control
- Google Drive for large model storage

# How to Use

1. Clone the repository:
   ```
   git clone https://github.com/your-username/vakilbot.git
   ```
2. Set up the environment:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```

4. Upload a PDF file and receive a simplified summary of its legal content.

# License

This project is for educational and research purposes only.
