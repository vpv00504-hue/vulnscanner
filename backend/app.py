from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# fix path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.predict import predict

app = Flask(__name__)
CORS(app)


@app.route("/predict", methods=["POST"])
def run():
    try:
        code = request.json.get("code", "")

        if not code.strip():
            return jsonify({"result": "❌ No code provided"}), 400

        result = predict(code)

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"result": f"❌ Server Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(port=5000)