from typing import List, Tuple

class ChatMemory:
    """
    Sliding-window memory that keeps the last `max_turns` (user, bot) exchanges.
    """
    def __init__(self, max_turns: int = 4):
        self.max_turns = max(1, int(max_turns))
        self.history: List[Tuple[str, str]] = []

    def add_turn(self, user_input: str, bot_response: str) -> None:
        self.history.append((user_input.strip(), bot_response.strip()))
        if len(self.history) > self.max_turns:
            # drop the oldest turn
            self.history.pop(0)

    def render_context(self) -> str:
        """
        Render the conversation in a simple, consistent format.
        Example:
        User: Hi
        Bot: Hello!
        User: How are you?
        Bot: I'm good.
        """
        lines = []
        for u, b in self.history:
            lines.append(f"User: {u}")
            lines.append(f"Bot: {b}")
        return "\n".join(lines)
