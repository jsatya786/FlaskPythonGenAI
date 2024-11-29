from flask import Blueprint, render_template, request
import requests

text_generation_bp = Blueprint('text_generation', __name__)

@text_generation_bp.route('/', methods=['GET', 'POST'])
def text_generation():
    generated_text = ""
    if request.method == 'POST':
        prompt = request.form['prompt']
        api_url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Authorization": "Bearer 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"}
        payload = {"inputs": prompt}

        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            generated_text = response.json()[0]['generated_text']
        else:
            generated_text = "Error: Unable to generate text."

    return render_template('text_generation.html', generated_text=generated_text)