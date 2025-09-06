import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import truncate_tweet


def test_no_truncation_when_short():
    text = "Hello world"
    assert truncate_tweet(text, limit=50) == text


def test_truncation_respects_word_boundary():
    text = "hello world this is a test"
    assert truncate_tweet(text, limit=17) == "hello world this"


def test_truncation_without_spaces():
    text = "a" * 200
    result = truncate_tweet(text, limit=50)
    assert len(result) <= 50
