import requests
from PIL import Image
from io import BytesIO
import ssl
import time
from flask import Blueprint, render_template, request
import io
import base64

text_to_image_bp = Blueprint('text_to_image', __name__)
#generate_image_bp = Blueprint('generate_image', __name__)

@text_to_image_bp.route('/',methods=['GET','POST'])
def text_to_image():
    img_base64=""
    if request.method == 'POST':
        prompt = request.form['prompt']
        image = generate_image_from_text(prompt)
        
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        # Convert BytesIO to base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return render_template('text_to_image.html', img_data=img_base64)

#@generate_image_from_text.route('/generate_image', methods=['POST'])
def generate_image():
    prompt = request.form['prompt']
    image = generate_image_from_text(prompt)
    
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    # Convert BytesIO to base64
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    
    return render_template('text_to_image.html', img_data=img_base64)

# Bypass SSL certificate authentication
ssl._create_default_https_context = ssl._create_unverified_context

def generate_image_from_text(prompt):
    api_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
    headers = {"Authorization": "Bearer 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"}
    payload = {"inputs": prompt}
    
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            return image
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            if response.status_code == 500:
                warnings = response.json().get("warnings", [])
                for warning in warnings:
                    print(warning)
                print("Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
        except Exception as err:
            print(f"An error occurred: {err}")
            break
    return None

if __name__ == "__main__":
    prompt = "A fantasy landscape with mountains and a river"
    image = generate_image_from_text(prompt)
    if image:
        image.show()
    else:
        print("Failed to generate image.")