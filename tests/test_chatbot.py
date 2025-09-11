import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot import Chatbot, ollama
from utils import MAX_TWEET_LEN, truncate_tweet

def test_context_keeps_last_three_interactions(monkeypatch):
    captured = {}

    def fake_chat(model, messages):
        captured['messages'] = messages
        return {'message': {'content': 'ok'}}

    monkeypatch.setattr(ollama, 'chat', fake_chat)
    bot = Chatbot(model='test')
    for i in range(5):
        bot.generate(f'msg{i}')
    assert len(bot.history) == 10
    assert len(captured['messages']) == 8  # system + 3 interactions *2 + new user
    assert captured['messages'][1]['content'] == 'msg1'
    assert captured['messages'][-1]['content'] == 'msg4'

def test_long_answer_is_rewritten_until_short(monkeypatch):
    calls = []

    responses = ['x' * 200, 'y' * 190, 'short response']

    def fake_chat(model, messages):
        calls.append(messages)
        return {'message': {'content': responses[len(calls) - 1]}}

    monkeypatch.setattr(ollama, 'chat', fake_chat)
    bot = Chatbot(model='test')
    reply = bot.generate('hi')
    assert reply == 'short response'
    assert len(calls) == 3
    # ensure each follow-up call asks to rewrite
    for msgs in calls[1:]:
        assert any('rewrite the above answer' in m['content'] for m in msgs if m['role'] == 'user')


def test_truncates_and_warns_when_model_never_shortens(monkeypatch, capsys):
    long_text = "lorem ipsum " * 20

    def fake_chat(model, messages):
        return {'message': {'content': long_text}}

    monkeypatch.setattr(ollama, 'chat', fake_chat)
    bot = Chatbot(model='test')
    reply = bot.generate('hi')
    captured = capsys.readouterr()
    assert reply == truncate_tweet(long_text)
    assert 'Warning: response exceeds' in captured.out