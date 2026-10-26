import json
import os
import requests

# Fail-safe import for validator across different execution modes
try:
    from core.validator import HTMLValidator
except ImportError:
    try:
        from .validator import HTMLValidator
    except ImportError:
        from validator import HTMLValidator

class MetaAIGenerator:
    def __init__(self, config_path="config.json"):
        # Safe config loading
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception:
                self.config = {}
        else:
            self.config = {}
        
        self.api_key = self.config.get("meta_api_key", "")
        self.api_url = "https://api.meta.ai/v1/chat/completions"
        self.validator = HTMLValidator()

    def call_meta_api(self, prompt, business_name="Local Business"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "muse-spark-1.3",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an elite web developer. Output clean, valid, single-file HTML5 landing pages using Tailwind CSS CDN."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }

        # If API key is missing, placeholder, or empty, instantly use offline mode to prevent hanging
        if not self.api_key or "YOUR_KEY" in self.api_key or len(self.api_key.strip()) == 0:
            print("   [Info] Using local offline template generation (API key not active).", flush=True)
            return self.get_fallback_html(business_name)

        try:
            print("   [Network] Sending request to Meta Model API...", flush=True)
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return self.clean_code_output(content)
            else:
                print(f"   [API Warning {response.status_code}] Falling back to local template.", flush=True)
                return self.get_fallback_html(business_name)
        except Exception as e:
            print(f"   [Connection Timeout/Error] Falling back to local template: {str(e)}", flush=True)
            return self.get_fallback_html(business_name)

    def clean_code_output(self, raw_text):
        text = raw_text.strip()
        if text.startswith("```html"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def get_fallback_html(self, business_name):
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{business_name} | Professional Services</title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans">
    <header class="bg-blue-600 text-white p-6 shadow-md text-center">
        <h1 class="text-3xl font-bold">{business_name}</h1>
        <p class="mt-2 text-blue-100">Your Trusted Local Experts</p>
    </header>
    <main class="max-w-4xl mx-auto p-8 text-center">
        <h2 class="text-2xl font-semibold mb-4">Welcome to Our New Online Home</h2>
        <p class="text-lg text-slate-600 mb-6">We provide top-tier professional services right here in your community.</p>
        <a href="#contact" class="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium shadow hover:bg-blue-700">Contact Us Today</a>
    </main>
</body>
</html>"""

    def generate_with_self_correction(self, lead_data, max_retries=3):
        business_name = lead_data.get("name", "Local Business")
        category = lead_data.get("category", "Services")
        location = lead_data.get("location", "Local Area")
        phone = lead_data.get("phone", "Contact Us")

        base_prompt = (
            f"Create a high-converting, professional single-page website for '{business_name}', "
            f"a business in the '{category}' sector located in '{location}'. "
            f"Phone contact: {phone}. "
            f"Include a modern hero section, services list, about section, and contact footer. "
            f"Use Tailwind CSS via CDN for all styling. Ensure <html>, <body>, and <title> tags are present."
        )

        current_prompt = base_prompt

        for attempt in range(1, max_retries + 1):
            print(f"   [Generator] Attempt {attempt} of {max_retries} for {business_name}...", flush=True)
            
            html_code = self.call_meta_api(current_prompt, business_name=business_name)
            is_valid, error_msg = self.validator.validate_html(html_code)

            if is_valid:
                print(f"   [Success] Code generated and verified for {business_name}!", flush=True)
                return html_code
            else:
                print(f"   [Validation Warning] Attempt {attempt} failed: {error_msg}", flush=True)
                current_prompt = (
                    f"{base_prompt}\n\n"
                    f"PREVIOUS ATTEMPT FAILED VALIDATION WITH ERROR: {error_msg}. "
                    f"Fix this error and output complete, flawless HTML."
                )

        return self.get_fallback_html(business_name)