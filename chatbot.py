"""Chatbot using Ollama to generate concise English responses."""
from typing import List, Dict

try:
    import ollama  # type: ignore
except Exception:  # pragma: no cover - library may not be installed
    class _OllamaFallback:
        """Fallback that raises if Ollama is unavailable."""
        def chat(self, *args, **kwargs):
            raise RuntimeError("Ollama library is required to run this chatbot.")
    ollama = _OllamaFallback()

from utils import truncate_tweet, MAX_TWEET_LEN

class Chatbot:
    """A simple conversational agent that maintains short context."""

    def __init__(self, model: str = "llama2") -> None:
        self.model = model
        self.history: List[Dict[str, str]] = []

    def _build_messages(self, user_input: str) -> List[Dict[str, str]]:
        """Prepare messages with system prompt and limited context."""
        system = {
            "role": "system",
            "content": (
                "You are a chatbot that always responds in clear, correct English. "
                f"Each response must be a complete idea, maximum {MAX_TWEET_LEN} characters. "
                f"Never exceed {MAX_TWEET_LEN} characters. Never truncate mid-thought. "
                f"If you cannot answer fully within {MAX_TWEET_LEN} characters, rephrase concisely."
                "Your responses must be consistent with previous context."
            ),
        }
        context = self.history[-6:]  # last 3 interactions (user+assistant)
        messages = [system] + context + [{"role": "user", "content": user_input}]
        return messages

    def generate(self, user_input: str) -> str:
        """Generate a response and update history."""
        messages = self._build_messages(user_input)

        attempts = 0
        while True:
            response = ollama.chat(model=self.model, messages=messages)
            text = response["message"]["content"].strip()
            if len(text) <= MAX_TWEET_LEN:
                break
            attempts += 1
            if attempts >= 3:
                print(
                    f"Warning: response exceeds {MAX_TWEET_LEN} characters; truncating."
                )
                text = truncate_tweet(text)
                break
            print(f"Response too long ({len(text)} chars); asking to rewrite.")
            messages.extend(
                [
                    {"role": "assistant", "content": text},
                    {
                        "role": "system",
                        "content": (
                            # "Your last answer was too long. "
                            f"Rewrite your last answer under {MAX_TWEET_LEN} characters."
                            "Give the full idea in that limit."
                            "Give ONLY the final answer, no preamble, no explanations."
                        ),
                    },
                ]
            )

        text = truncate_tweet(text)
        self.history.extend(
            [{"role": "user", "content": user_input}, {"role": "assistant", "content": text}]
        )
        return text

    def display_history(self) -> None:
        """Print the conversation history."""
        for msg in self.history:
            prefix = "User" if msg["role"] == "user" else "Bot"
            print(f"{prefix}: {msg['content']}")
