import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.predict import predict


def run_model(code):
    result = predict(code, return_json=True)

    # convert to frontend-friendly format
    status = "⚠️ Vulnerable Code" if result["is_vulnerable"] else "✅ Safe Code"

    return {
        "status": status,
        "safe": result["safe"],
        "vulnerable": result["vulnerable"],
        "explanation": result["explanation"],
        "time": result["time"]
    }