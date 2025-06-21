from transformers import pipeline

# Load more powerful model for free
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def chunk_text(text, chunk_size=1000):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def generate_summary(text, max_length=250, min_length=80):
    if len(text.split()) < 300:
        return "⚠️ The text is already concise. No summarization needed."

    chunks = chunk_text(text, chunk_size=1000)
    final_summary = ""

    for chunk in chunks[:3]:
        summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
        final_summary += summary + "\n\n"

    return final_summary.strip()
