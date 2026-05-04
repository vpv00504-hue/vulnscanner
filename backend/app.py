from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import your model function
from scripts.predict import predict

app = Flask(__name__)
CORS(app)

# 🔥 Load model once (IMPORTANT for speed)
print("🚀 Loading model once...")
model_loaded = True   # just a flag (your predict already loads internally)

@app.route("/")
def home():
    return "✅ VulnScanner Backend Running"

@app.route("/predict", methods=["POST"])
def run():
    try:
        data = request.get_json()

        if not data or "code" not in data:
            return jsonify({"error": "No code provided"}), 400

        code = data["code"]

        if not code.strip():
            return jsonify({"error": "Empty code"}), 400

        result = predict(code)

        return jsonify({
            "status": "success",
            "prediction": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 🔥 VERY IMPORTANT FOR DEPLOYMENT
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)