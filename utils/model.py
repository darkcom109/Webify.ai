import re
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

def generate():
    """Generate HTML body content only, with auto-cleaning of unwanted tags."""
    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct:cerebras",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a website generator. "
                    "Output ONLY the content that belongs inside an HTML <body> tag. "
                    "Do NOT include <!DOCTYPE html>, <html>, <head>, or <title> tags. "
                    "Do NOT include explanations, comments, or markdown code fences. "
                    "Stop after your last closing tag."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Generate a playful, colorful landing page with:\n"
                    "- A big heading\n"
                    "- A short tagline\n"
                    "- A button that changes colors using JavaScript\n"
                    "- A few random emojis or images for fun\n"
                    "Use inline <style> and <script> tags if needed."
                ),
            },
        ],
        stop=["</html>", "```", "<html", "<!DOCTYPE"],  # stop sequences to cut off extra
    )

    raw = completion.choices[0].message.content

    # Force-strip forbidden tags
    clean = re.sub(r"<!DOCTYPE.*?>", "", raw, flags=re.IGNORECASE | re.DOTALL)
    clean = re.sub(r"<html.*?>|</html>", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"<head.*?>.*?</head>", "", clean, flags=re.IGNORECASE | re.DOTALL)
    clean = clean.strip()

    # Extract only <body> inner content if present
    match = re.search(r"<body[^>]*>(.*?)</body>", clean, flags=re.IGNORECASE | re.DOTALL)
    if match:
        clean = match.group(1).strip()

    print(clean)
    return clean

