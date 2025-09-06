import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot import Chatbot, ollama


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
