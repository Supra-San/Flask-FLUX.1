from flask import Flask, render_template, request, redirect, url_for
import requests
import io
import base64
from PIL import Image
import os

#import config
from config.config import API_URL, API_TOKEN

app = Flask(__name__)

def query(payload):
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if not prompt:
            return render_template('index.html', error='Please enter your prompt')
        
        payload = {
            "inputs": prompt
        }

        image_bytes = query(payload)

        if image_bytes:
            image = Image.open(io.BytesIO(image_bytes))
            buffered = io.BytesIO()
            image.save(buffered, format='PNG')
            img_str = base64.b64encode(buffered.getvalue()).decode()
            img_data = f"data:image/png;base64,{img_str}"
            return render_template('index.html', image=img_data)
        else:
            return render_template('index.html', error='Failed load the image')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)