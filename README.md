# Local CLI Chatbot (Hugging Face)

A simple command-line chatbot that runs locally using a small Hugging Face text-generation model.
It maintains short-term memory with a sliding window for coherent multi-turn conversation.

## Folder Structure

```text
chatbot/
├─ model_loader.py      # Model & tokenizer loading via HF pipeline
├─ chat_memory.py       # Sliding window memory buffer
├─ interface.py         # CLI loop and integration
├─ requirements.txt     # Dependencies
└─ README.md            # Setup, run, and examples
```

## Setup

1. **Create & activate a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

> If PyTorch wheel resolution fails, visit https://pytorch.org/get-started/locally/ for a platform-specific install,
> then rerun `pip install -r requirements.txt`.

## Run

```bash
python interface.py
```

Optional: choose a different model (must be a small causal LM) via env var:
```bash
set HF_MODEL=distilgpt2         # Windows (cmd)
export HF_MODEL=distilgpt2      # macOS/Linux
python interface.py
```

## Example

```text
🤖 Local HF Chatbot ready! Type /exit to quit.

User: What is the capital of France?
Bot: The capital of France is Paris.

User: And what about Italy?
Bot: The capital of Italy is Rome.

User: /exit
Bot: Exiting chatbot. Goodbye!
```

## Design Notes

- **HF pipeline** keeps the code minimal while letting you swap small models easily.
- **Sliding window** memory (default 4 turns) keeps recent context without runaway prompts.
- **Prompt format** uses `User:`/`Bot:` markers to help the model separate turns.
- **Heuristic cleanup** trims the reply and stops at the next `User:` marker if generated.

## Troubleshooting

- *It prints weird or repeats the prompt*: reduce `max_new_tokens` or temperature.
- *GPU not used*: this demo is CPU-friendly. If you have a CUDA GPU and a matching torch build, the pipeline may use it automatically.
- *Model download slow*: first run downloads weights to your HF cache; subsequent runs are fast.
