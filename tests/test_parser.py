"""
Simple tests for the RSS transformer
"""

import sys
import os

# Add parent directory to path so we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import extract_show_name, normalize_show_name, parse_episodes
from src.generator import format_show_title


def test_normalize_show_name():
    """Test show name normalization."""
    assert normalize_show_name("Dimension 20") == "dimension-20"
    assert normalize_show_name("Game Changer") == "game-changer"
    assert normalize_show_name("Um, Actually?") == "um-actually"
    assert normalize_show_name("Breaking News!!!") == "breaking-news"
    print("✓ test_normalize_show_name passed")


def test_extract_show_name():
    """Test show name extraction from titles."""
    assert extract_show_name("Dimension 20: Fantasy High") == "dimension-20"
    assert extract_show_name("Game Changer - New Episode") == "game-changer"
    assert extract_show_name("[Um, Actually] Season Finale") == "um-actually"
    print("✓ test_extract_show_name passed")


def test_format_show_title():
    """Test show title formatting."""
    assert format_show_title("dimension-20") == "Dimension 20"
    assert format_show_title("game-changer") == "Game Changer"
    assert format_show_title("um-actually") == "Um Actually"
    print("✓ test_format_show_title passed")


def test_parse_empty_feed():
    """Test parsing an empty feed."""
    episodes = parse_episodes("")
    assert isinstance(episodes, list)
    assert len(episodes) == 0
    print("✓ test_parse_empty_feed passed")


if __name__ == '__main__':
    print("Running tests...")
    test_normalize_show_name()
    test_extract_show_name()
    test_format_show_title()
    test_parse_empty_feed()
    print("\n✅ All tests passed!")
