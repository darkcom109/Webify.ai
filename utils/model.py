import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # will read .env and populate os.environ

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

def generate():
    completion = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct:cerebras",
        messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a code generator. Output ONLY valid HTML code. "
                        "Do not include explanations, comments, or Markdown code fences. "
                        "Do not insert the DOCTYPE JUST THE HTML CODE ITSELF"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Generate a fun and random website. It should have:\n"
                        "- A colorful background\n"
                        "- A large creative heading\n"
                        "- A short tagline or description\n"
                        "- At least one button that does something funny with JavaScript (like changing colors or text)\n"
                        "- Some random images or emojis\n"
                        "Keep everything in one HTML file with inline CSS and JS. Make it playful and different every time."
                    ),
                },
            ],
    )
    return completion.choices[0].message.content
