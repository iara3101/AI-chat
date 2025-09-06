"""Utility helpers for tweet-sized responses."""
from __future__ import annotations

MAX_TWEET_LEN = 180


def truncate_tweet(text: str, limit: int = MAX_TWEET_LEN) -> str:
    """Truncate text at a word boundary without exceeding the limit."""
    if len(text) <= limit:
        return text
    truncated = text[:limit]
    cut_index = -1
    for ch in [" ", ",", ".", "?", "!", ";", ":"]:
        idx = truncated.rfind(ch)
        if idx > cut_index:
            cut_index = idx
    if cut_index == -1:
        return truncated.rstrip()
    return truncated[:cut_index].rstrip()
