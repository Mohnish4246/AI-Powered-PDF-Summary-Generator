#  AI-Powered PDF Summary Generator

An intelligent web application that allows users to upload PDF documents and receive a clean, concise summary powered by a transformer-based AI model. Built using **Streamlit** and **Hugging Face Transformers**, this tool is ideal for summarizing reports, research papers, academic articles, and more.

---

##  Features

-  Upload and extract text from PDF files  
-  Summarize long documents using **facebook/bart-large-cnn** model  
-  Choose summary length: Short / Medium / Long  
-  Automatically cleans smart quotes, emojis, and special characters  
-  Read the summary aloud using **Text-to-Speech** (`pyttsx3`)  
-  Download summary as `.txt` or `.pdf`  
-  Optional: Download summary as `.mp3` using `gTTS`  
-  Word cloud of key summary terms (optional)

---

##  Tech Stack

| Component         | Tool/Library           |
|------------------|------------------------|
| Web App          | Streamlit              |
| Summarization    | Hugging Face Transformers (`facebook/bart-large-cnn`)  
| PDF Extraction   | PyMuPDF (`fitz`)       |
| PDF Generator    | FPDF                   |
| Text Cleanup     | Regex + Preprocessing  |
| TTS (Offline)    | pyttsx3                |
| TTS (Download)   | gTTS (optional)        |
| Visualization    | WordCloud, Matplotlib  |

---

##  Installation

```bash
git clone https://github.com/your-username/pdf-summary-ai.git
cd pdf-summary-ai

# Optional: Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install all dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
