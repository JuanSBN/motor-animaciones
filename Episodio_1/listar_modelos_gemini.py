import os
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from google import genai

api_key = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key)

print("Listando modelos disponibles para esta API Key...")
models = client.models.list()
for m in models:
    name = getattr(m, 'name', '') or str(m)
    # Check if supports audio or modalities
    modalities = getattr(m, 'supported_generation_methods', [])
    print(f"- {name} (methods: {modalities})")
