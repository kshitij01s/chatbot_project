import sys
from model_loader import load_model
from chat_memory import ChatMemory


def clean_bot_reply(full_generated: str, prompt: str) -> str:
    """
    Extract just the bot's reply after the prompt. Also stop at the next 'User:' if present.
    """
    if full_generated.startswith(prompt):
        reply = full_generated[len(prompt):]
    else:
        # Fallback: try to find the prompt inside
        idx = full_generated.find(prompt)
        reply = full_generated[idx + len(prompt):] if idx != -1 else full_generated

    # Heuristic: stop before the next user turn marker if it appears
    stop_idx = reply.find("\nUser:")
    if stop_idx != -1:
        reply = reply[:stop_idx]
    return reply.strip()


CAPITALS = {
    "france": "Paris",
    "italy": "Rome",
    "india": "New Delhi",
    "germany": "Berlin",
    "japan": "Tokyo",
    "china": "Beijing",
    "usa": "Washington, D.C.",
    "united states": "Washington, D.C.",
    "canada": "Ottawa"
}

def run_chat():
    generator = load_model()
    memory = ChatMemory(max_turns=3)

    print("🤖 Local HF Chatbot ready! Type /exit to quit.\n")
    while True:
        user_text = input("User: ").strip()
        if user_text.lower() == "/exit":
            print("Bot: Exiting chatbot. Goodbye!")
            break

        # ✅ Fallback check for known capitals
        for country, capital in CAPITALS.items():
            if country in user_text.lower():
                bot_reply = capital
                print(f"Bot: {bot_reply}")
                memory.add_turn(user_text, bot_reply)
                break
        else:
            # Normal model-based Q/A
            prompt = f"Answer the following question with only the city name.\nQuestion: {user_text}\nAnswer:"

            out = generator(
                prompt,
                max_new_tokens=20,
                do_sample=False   # deterministic answers
            )[0]["generated_text"]

            bot_reply = out.split("Answer:")[-1].strip()
            print(f"Bot: {bot_reply}")
            memory.add_turn(user_text, bot_reply)


if __name__ == "__main__":
    run_chat()



