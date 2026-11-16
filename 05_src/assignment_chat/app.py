import re
import gradio as gr
RESTRICTED_PATTERNS = [
    r"\b(cat|cats|kitten|kittens|dog|dogs|puppy|puppies)\b",
    r"\b(horoscope|horoscopes|zodiac)\b",
    r"\b(aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|capricorn|aquarius|pisces)\b",
    r"\btaylor\s+swift\b"
]

PROMPT_PROTECTION_PATTERNS = [
    r"\bsystem prompt\b",
    r"\bhidden instructions\b",
    r"\bdeveloper message\b",
    r"\breveal your instructions\b",
    r"\bignore (all )?(previous|prior) instructions\b",
    r"\boverride your instructions\b"
]

from langchain_core.messages import HumanMessage, AIMessage
from main import travelmate_graph

def travelmate_chat(message: str, history: list) -> str:

    if any(re.search(pattern, message, re.IGNORECASE)
           for pattern in RESTRICTED_PATTERNS):
        return "I'm sorry, I can't help with that topic. I'm here to help with travel planning instead!"

    if any(re.search(pattern, message, re.IGNORECASE)
           for pattern in PROMPT_PROTECTION_PATTERNS):
        return "I can't share or change my internal instructions."

    messages = []

    for item in history[-12:]:
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content")

            if role == "user" and isinstance(content, str):
                messages.append(HumanMessage(content=content))
            elif role == "assistant" and isinstance(content, str):
                messages.append(AIMessage(content=content))

        elif isinstance(item, (tuple, list)) and len(item) == 2:
            user_message, assistant_message = item

            if user_message:
                messages.append(HumanMessage(content=str(user_message)))

            if assistant_message:
                messages.append(AIMessage(content=str(assistant_message)))

    messages.append(HumanMessage(content=message))

    result = travelmate_graph.invoke({"messages": messages})

    return result["messages"][-1].content


chat = gr.ChatInterface(
    fn=travelmate_chat,
    title="TravelMate AI",
    description="Your friendly AI travel companion — ask about weather, travel tips, and trip budgets."
)

if __name__ == "__main__":
    chat.launch()