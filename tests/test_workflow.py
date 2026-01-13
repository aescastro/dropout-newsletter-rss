"""
Test the full transformation workflow with mock data
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import parse_episodes, group_episodes_by_show
from src.generator import generate_rss_feed, generate_all_shows_feed


# Mock RSS feed content
MOCK_RSS_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Dropout Newsletter</title>
    <link>https://kill-the-newsletter.com/</link>
    <description>Newsletter feed</description>
    <item>
      <title>Dimension 20: Fantasy High - Episode 1</title>
      <description>The Bad Kids start their adventure at Aguefort Adventuring Academy.</description>
      <link>https://example.com/d20-1</link>
      <pubDate>Mon, 10 Jan 2026 10:00:00 GMT</pubDate>
      <guid>d20-ep1</guid>
    </item>
    <item>
      <title>Game Changer - Season 6 Premiere</title>
      <description>New season of the game show where the game changes every episode!</description>
      <link>https://example.com/gc-1</link>
      <pubDate>Mon, 10 Jan 2026 15:00:00 GMT</pubDate>
      <guid>gc-ep1</guid>
    </item>
    <item>
      <title>Dimension 20: Fantasy High - Episode 2</title>
      <description>The Bad Kids face their first major challenge.</description>
      <link>https://example.com/d20-2</link>
      <pubDate>Tue, 11 Jan 2026 10:00:00 GMT</pubDate>
      <guid>d20-ep2</guid>
    </item>
  </channel>
</rss>"""


def test_full_workflow():
    """Test the complete transformation workflow."""
    print("Testing full workflow with mock data...")
    
    # Parse episodes
    episodes = parse_episodes(MOCK_RSS_FEED)
    print(f"✓ Parsed {len(episodes)} episodes")
    assert len(episodes) == 3
    
    # Group by show
    shows = group_episodes_by_show(episodes)
    print(f"✓ Grouped into {len(shows)} shows: {list(shows.keys())}")
    assert 'dimension-20' in shows
    assert 'game-changer' in shows
    assert len(shows['dimension-20']) == 2
    assert len(shows['game-changer']) == 1
    
    # Generate per-show feed
    d20_feed = generate_rss_feed('dimension-20', shows['dimension-20'])
    print(f"✓ Generated Dimension 20 feed ({len(d20_feed)} chars)")
    assert '<title>Dimension 20</title>' in d20_feed
    assert 'Fantasy High - Episode 1' in d20_feed
    assert 'Fantasy High - Episode 2' in d20_feed
    
    gc_feed = generate_rss_feed('game-changer', shows['game-changer'])
    print(f"✓ Generated Game Changer feed ({len(gc_feed)} chars)")
    assert '<title>Game Changer</title>' in gc_feed
    assert 'Season 6 Premiere' in gc_feed
    
    # Generate all-shows feed
    all_feed = generate_all_shows_feed(episodes)
    print(f"✓ Generated all-shows feed ({len(all_feed)} chars)")
    assert '<title>Dropout - All Shows</title>' in all_feed
    assert 'Fantasy High' in all_feed
    assert 'Game Changer' in all_feed
    
    # Test writing to files
    output_dir = Path('/tmp/test-workflow-feeds')
    output_dir.mkdir(exist_ok=True)
    
    d20_path = output_dir / 'dimension-20.xml'
    with open(d20_path, 'w') as f:
        f.write(d20_feed)
    print(f"✓ Wrote feed to {d20_path}")
    assert d20_path.exists()
    
    all_path = output_dir / 'all-shows.xml'
    with open(all_path, 'w') as f:
        f.write(all_feed)
    print(f"✓ Wrote feed to {all_path}")
    assert all_path.exists()
    
    print("\n✅ Full workflow test passed!")


if __name__ == '__main__':
    test_full_workflow()
