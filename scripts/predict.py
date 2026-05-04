import torch
import requests
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.gnn_model import VulnGNN
from utils.preprocess_single import preprocess_code

MODEL_PATH = "models/saved/best_model.pth"

print("🚀 Loading GNN model...")
model = VulnGNN()
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()
print("✅ Model Ready!")


def explain_with_ollama(code):
    prompt = f"""
You are a cybersecurity expert.

Analyze this C code:

{code}

Explain:
1. Is it vulnerable?
2. Why?
3. Provide fixed safe code.
"""

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False}
        )
        return res.json().get("response", "No explanation")
    except:
        return "⚠️ Ollama not running"


def predict(code_snippet):
    start = time.time()

    data = preprocess_code(code_snippet)

    cls = data.cls
    if cls.dim() == 1:
        cls = cls.unsqueeze(0)

    with torch.no_grad():
        out = model(data, cls)
        probs = torch.softmax(out, dim=1).numpy()[0]

    safe_prob = probs[0]
    vuln_prob = probs[1]

    # calibration
    vuln_prob *= 0.85
    safe_prob *= 1.15
    total = safe_prob + vuln_prob
    safe_prob /= total
    vuln_prob /= total

    score = vuln_prob - safe_prob

    result = ""

    if score > 0.3:
        result += "⚠️ Vulnerable Code\n"
    else:
        result += "✅ Safe Code\n"

    result += f"\nSafe: {safe_prob:.4f}"
    result += f"\nVulnerable: {vuln_prob:.4f}"

    if score > 0.3:
        explanation = explain_with_ollama(code_snippet)
        result += "\n\n🧠 Explanation:\n" + explanation

    result += f"\n\n⚡ Time: {time.time() - start:.2f} sec"

    return result