import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API Key and Endpoint
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# Debugging logs
print(f"DEBUG: API_KEY={API_KEY}")
print(f"DEBUG: ENDPOINT={ENDPOINT}")

if not API_KEY or not ENDPOINT:
    raise ValueError("Missing API key or endpoint in environment variables.")

# Initialize Flask app
app = Flask(__name__)

# Function to call Azure AI Foundry
def analyze_clause(text):
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
        "x-ms-model-mesh-model-name": "Mistral-small"  # Specify the model name in the header
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a legal assistant that analyzes contract clauses."},
            {"role": "user", "content": text}
        ]
    }
    response = requests.post(
        ENDPOINT,
        headers=headers,
        json=payload
    )
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json()}

@app.route("/", methods=["GET", "POST"])
def index():
    """Render a description and form for the app."""
    if request.method == "POST":
        clause = request.form.get("clause")
        if not clause:
            return jsonify({"error": "No clause provided."}), 400
        result = analyze_clause(clause)
        return jsonify(result)
    return '''
        <h1>Welcome to ClauseCat</h1>
        <p>This application is designed to analyze legal contract clauses using the Mistral Small model hosted on Azure AI Foundry.</p>
        <p>To use this app:</p>
        <ol>
            <li>Enter a legal clause in the box below.</li>
            <li>Click "Analyze Clause".</li>
            <li>Review the analysis results.</li>
        </ol>
        <form method="POST">
            <textarea name="clause" rows="5" cols="50" placeholder="Enter a legal clause here..."></textarea><br><br>
            <button type="submit">Analyze Clause</button>
        </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
