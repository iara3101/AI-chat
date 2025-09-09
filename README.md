# AI Chat with Ollama

This project demonstrates a conversational chatbot powered by [Ollama](https://ollama.com/).
Responses are tweet-sized (maximum 180 characters). The bot keeps rewriting overly long answers until they fit, and if
shortening fails after several tries it warns and truncates the reply at a word boundary.

## Features
- Maintains context for the last three interactions
- Ensures replies are in English with correct grammar
- Iteratively rewrites any answer exceeding 180 characters and warns with a word-boundary truncated reply if shortening fails
- Command line interface with visible conversation history

## Requirements
- Python 3.10+
- A running [Ollama](https://ollama.com/) server with a suitable model (e.g., `llama2`)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage
Start the chat:

```bash
python main.py
```
Type messages and the bot will answer in tweet format. Use `exit` to quit; the
full conversation history will then be displayed.

## Testing
Run unit tests with:

```bash
pytest
```


## Traubleshooting

### Installing Ollama
Steps to run Ollama with llama2 in a GitHub Codespace

1. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Start the server (background)

```bash
ollama serve &
```
3. Download the model

```bash
ollama pull llama2
```
4. Verify

```bash
ollama run llama2 "Hello!"
```
5. Expose port 11434
Forward it in your Codespace so your app can reach the server.