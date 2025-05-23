from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Initialize GPT-2 text generator once
generator = pipeline('text-generation', model='gpt2')

def generate_marketing_copy(prompt, creativity=1.0):
    outputs = generator(prompt, max_length=100, num_return_sequences=1, temperature=creativity)
    return outputs[0]['generated_text']

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    creativity = 1.0  # default creativity value
    if request.method == "POST":
        product = request.form.get("product")
        tone = request.form.get("tone")
        audience = request.form.get("audience")
        creativity_str = request.form.get("creativity", "1.0")

        # Validate and convert creativity input safely
        try:
            creativity = float(creativity_str)
            if creativity < 0.1 or creativity > 2.0:
                creativity = 1.0
        except ValueError:
            creativity = 1.0

        prompt = (
            f"Write a marketing copy for a product: {product}, "
            f"with a tone: {tone}, "
            f"targeting this audience: {audience}."
        )

        result = generate_marketing_copy(prompt, creativity)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)

