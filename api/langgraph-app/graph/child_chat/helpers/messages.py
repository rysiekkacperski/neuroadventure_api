# Implement logic to format messages (e.g., "Human: ...", "AI: ...") and potentially truncate history to avoid overly long prompts
def format_messages_for_prompt(messages: list):
    history_str = ""
    for msg in reversed(messages): # Often good to have recent messages last
        if hasattr(msg, 'type'):
            speaker = "AI" if msg.type == "ai" else "Human"
            history_str = f"{speaker}: {msg.content}\n" + history_str
    return history_str