from transformers import pipeline
import os

def load_model(model_name: str | None = None):
    model_name = model_name or os.getenv("HF_MODEL", "google/flan-t5-small")

    # Use text2text-generation for T5 models
    if "t5" in model_name.lower():
        generator = pipeline("text2text-generation", model=model_name, tokenizer=model_name)
    else:
        generator = pipeline("text-generation", model=model_name, tokenizer=model_name)

    return generator
