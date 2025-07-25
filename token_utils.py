from transformers import AutoTokenizer
from dotenv import load_dotenv
import os

load_dotenv()
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise ValueError("Missing Hugging Face token. Set HF_TOKEN in your .env file.")

tokenizer = AutoTokenizer.from_pretrained(
    "google/gemma-2b",
    token=hf_token
)

# Count tokens for role + content
def count_tokens(messages):
    total_tokens = 0
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        tokenized = tokenizer.encode(f"{role}: {content}", add_special_tokens=False)
        total_tokens += len(tokenized)
    return total_tokens