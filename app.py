from flask import Flask, render_template, request, session
import anthropic
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key for session management

# Initialize Anthropic client
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []  # Initialize chat history if not present

    if request.method == "POST":
        user_input = request.form.get("question")
        # Store user input in the session
        session["chat_history"].append({"role": "user", "content": user_input})

        # Create a message to send to the Anthropic API
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": [{"type": "text", "text": user_input}]}
            ]
        )
        
        # Get the API response and store it in the session
        response_text = message.content[0].text
        session["chat_history"].append({"role": "assistant", "content": response_text})

    return render_template("index.html", chat_history=session["chat_history"])

@app.route("/clear")
def clear():
    session.pop("chat_history", None)  # Clear the chat history
    return render_template("index.html", chat_history=[])

if __name__ == "__main__":
    app.run(debug=True)
