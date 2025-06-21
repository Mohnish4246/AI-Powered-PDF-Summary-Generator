import streamlit as st
from pdf_reader import extract_text_from_pdf
from summarizer import generate_summary
import pyttsx3
from fpdf import FPDF
import io
import re

st.set_page_config(page_title="📄 PDF Summary Generator", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📄 AI-Powered PDF Summary Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload a PDF and get a concise, intelligent summary in seconds.</p>", unsafe_allow_html=True)

# ✅ Session State
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'text' not in st.session_state:
    st.session_state.text = None
if 'page_count' not in st.session_state:
    st.session_state.page_count = 0

# 🔧 Clean Text
def clean_text(text):
    replacements = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "…": "...",
        "•": "-",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)

    # 🧹 Remove emojis using regex
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map
                           u"\U0001F1E0-\U0001F1FF"  # flags
                           u"\U00002500-\U00002BEF"  # chinese char
                           u"\U00002702-\U000027B0"
                           u"\U0001F9E0"             # 🧠 brain (causing error)
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    
    return text

# 📝 Generate PDF
def create_pdf(summary_text):
    summary_text = clean_text(summary_text)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.set_text_color(0, 0, 128)
    pdf.cell(0, 10, "Summary", ln=True)  # 🔁 removed emoji
        
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    
    for line in summary_text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf_output = pdf.output(dest='S').encode('latin-1', 'replace')
    return io.BytesIO(pdf_output)

# 📤 Upload PDF
uploaded_file = st.file_uploader("📂 Upload your PDF file", type="pdf")

if uploaded_file:
    with st.spinner("📖 Extracting text from PDF..."):
        text, page_count, texts_by_page = extract_text_from_pdf(uploaded_file)
        st.session_state.text = text
        st.session_state.page_count = page_count
        st.success("✅ PDF loaded and processed!")
        st.info(f"📄 Total Pages: {page_count} | 📝 Word Count: {len(text.split())}")

    # Optional: Expand to show full extracted text
    with st.expander("🔍 View full extracted text"):
        st.text_area("📄 Preview Extracted Text", value=text[:3000], height=200)


summary_mode = st.radio(
    "📏 Choose Summary Length",
    ["Short", "Medium", "Long"],
    horizontal=True
)
st.info(f"📏 You selected: {summary_mode} summary mode.")

# 🔁 Set lengths based on mode
length_config = {
    "Short": (150, 50),
    "Medium": (250, 100),
    "Long": (350, 150)
}

# 🧠 Generate Summary
if st.button("✨ Summarize"):
    if not st.session_state.text:
        st.warning("⚠️ Please upload a PDF file first.")
    else:
        with st.spinner("🧠 Generating summary..."):
            max_len, min_len = length_config[summary_mode]
            try:
                summary = generate_summary(
                    st.session_state.text,
                    max_length=max_len,
                    min_length=min_len
                )
                st.session_state.summary = summary
            except Exception as e:
                st.error(f"❌ An error occurred while summarizing: {str(e)}")

# 💡 Display Summary
if st.session_state.summary:
    st.markdown("---")
    st.subheader("📌 Summary")
    st.write(st.session_state.summary)
    st.caption(f"📝 Summary Length: {len(st.session_state.summary.split())} words")

    # 📥 Download as TXT
    txt_data = "Summary\n\n" + st.session_state.summary  # 🔁 removed emoji
    st.download_button(
        label="📥 Download Summary as TXT",
        data=txt_data,
        file_name="summary.txt",
        mime="text/plain"
    )

    # 📥 Download as PDF
    pdf_bytes = create_pdf(st.session_state.summary)
    st.download_button(
        label="📄 Download as PDF",
        data=pdf_bytes,
        file_name="summary.pdf",
        mime="application/pdf"
    )

    # 🔊 Read Summary
    if st.button("🔊 Read Aloud"):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(st.session_state.summary)
        engine.runAndWait()
    st.caption("🔈 Note: Text-to-speech works only on local machines (not online hosts).")


# 📌 Footer
st.markdown("---")
st.markdown("<small style='text-align: center; display: block;'>Developed as part of Internship Project | AI PDF Summarizer</small>", unsafe_allow_html=True)