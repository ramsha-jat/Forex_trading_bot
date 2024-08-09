from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from openai import OpenAI
import google.generativeai as genai
import anthropic
import dotenv
import os
from PIL import Image
import base64
from io import BytesIO
import random

dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")
app.config['UPLOAD_FOLDER'] = 'uploads/'

anthropic_models = [
    "claude-3-5-sonnet-20240620"
]


def messages_to_anthropic(messages):
    # Same function as before
    pass


def stream_llm_response(model_params, model_type="openai", api_key=None):
    # Same function as before
    pass


def get_image_base64(image_raw):
    buffered = BytesIO()
    image_raw.save(buffered, format=image_raw.format)
    img_byte = buffered.getvalue()
    return base64.b64encode(img_byte).decode('utf-8')


def base64_to_image(base64_string):
    base64_string = base64_string.split(",")[1]
    return Image.open(BytesIO(base64.b64decode(base64_string)))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handling form submission for model selection and API keys
        anthropic_api_key = request.form.get("anthropic_api_key")
        model = request.form.get("model")
        temperature = float(request.form.get("temperature", 0.3))
        
        model_params = {
            "model": model,
            "temperature": temperature,
        }

        session["api_keys"] = {
            "anthropic": anthropic_api_key
        }
        session["model_params"] = model_params

        # Adding user message
        user_message = request.form.get("user_message")
        if user_message:
            session["messages"] = session.get("messages", [])
            session["messages"].append({"role": "user", "content": [{"type": "text", "text": user_message}]})
        
        # Adding image if uploaded
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(file_path)

                # Process image
                raw_img = Image.open(file_path)
                img = get_image_base64(raw_img)
                session["messages"].append({"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}}]})
        
        return redirect(url_for('index'))

    # Render the page with the messages and model options
    return render_template("index.html", messages=session.get("messages", []), models=anthropic_models )


@app.route("/reset", methods=["POST"])
def reset():
    session.pop("messages", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
