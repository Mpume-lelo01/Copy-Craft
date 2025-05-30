from flask import Flask, render_template, request, send_file
from transformers import pipeline, set_seed
from fpdf import FPDF
import os
import re

app = Flask(__name__)
generator = pipeline('text-generation', model='gpt2')
set_seed(42)

last_result = ""

def generate_marketing_copy(prompt, creativity=1.0):
    output = generator(prompt, max_length=100, num_return_sequences=1, temperature=creativity)
    return output[0]['generated_text'].strip()

def clean_text(text):
    # Replace common smart quotes and special chars with ASCII equivalents
    replacements = {
        '\u201c': '"',  # Left double quote
        '\u201d': '"',  # Right double quote
        '\u2018': "'",  # Left single quote
        '\u2019': "'",  # Right single quote
        '\u2013': '-',  # En dash
        '\u2014': '-',  # Em dash
        '\u2026': '...',  # Ellipsis
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Remove any other non-ASCII chars
    text = re.sub(r'[^\x00-\x7F]+','', text)
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    global last_result
    result = ""
    if request.method == "POST":
        product = request.form.get("product", "").strip()
        tone = request.form.get("tone", "").strip()
        audience = request.form.get("audience", "").strip()
        creativity = float(request.form.get("creativity", 1.0))

        prompt = f"Write a {tone} marketing copy for a product called '{product}', targeting {audience}."
        result = generate_marketing_copy(prompt, creativity)
        last_result = result

    return render_template("index.html", result=last_result)

@app.route("/download")
def download_pdf():
    global last_result
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Uncomment and add your PNG logo file (must be valid PNG) to static folder to enable logo
    # pdf.image("static/logo.png", x=10, y=8, w=30)

    cleaned_text = clean_text(last_result)
    for line in cleaned_text.split('\n'):
        pdf.multi_cell(0, 10, line)
        
    output_path = "static/generated_copy.pdf"
    pdf.output(output_path)
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
