"""Simple command line chat using Ollama."""
from chatbot import Chatbot


def main() -> None:
    bot = Chatbot()
    print("Type your message (or 'exit' to quit):")
    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        try:
            reply = bot.generate(user_input)
        except Exception as exc:  # pragma: no cover - depends on environment
            print(f"Error: {exc}")
            break
        print(f"Bot: {reply}")
    print("\nConversation history:")
    bot.display_history()


if __name__ == "__main__":
    main()
