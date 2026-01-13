"""
Parser module for extracting episodes and identifying shows from the RSS feed
"""

import feedparser
import re
from typing import List, Dict, Any
from datetime import datetime


def parse_episodes(feed_content: str) -> List[Dict[str, Any]]:
    """
    Parse RSS feed content and extract episodes with show information.
    
    Args:
        feed_content: Raw RSS feed XML content
        
    Returns:
        List of episode dictionaries with parsed information
    """
    feed = feedparser.parse(feed_content)
    episodes = []
    
    for entry in feed.entries:
        episode = {
            'title': entry.get('title', ''),
            'description': entry.get('description', '') or entry.get('summary', ''),
            'link': entry.get('link', ''),
            'pub_date': entry.get('published', '') or entry.get('updated', ''),
            'guid': entry.get('id', entry.get('link', '')),
        }
        
        # Extract show name from the title
        show_name = extract_show_name(episode['title'])
        episode['show_name'] = show_name
        
        episodes.append(episode)
    
    return episodes


def extract_show_name(title: str) -> str:
    """
    Extract the show name from an episode title.
    
    Common patterns in Dropout newsletters:
    - "Show Name: Episode Title"
    - "Show Name - Episode Title"
    - "[Show Name] Episode Title"
    
    Args:
        title: Episode title from the RSS feed
        
    Returns:
        Normalized show name (lowercase, hyphenated)
    """
    # Try different patterns to extract show name
    patterns = [
        r'^([^:]+):\s*',      # "Show Name: Episode"
        r'^([^-]+)-\s*',      # "Show Name - Episode"
        r'^\[([^\]]+)\]\s*',  # "[Show Name] Episode"
        r'^([^|]+)\|\s*',     # "Show Name | Episode"
    ]
    
    for pattern in patterns:
        match = re.match(pattern, title)
        if match:
            show_name = match.group(1).strip()
            return normalize_show_name(show_name)
    
    # If no pattern matches, try to identify known shows
    known_shows = {
        'dimension 20': 'dimension-20',
        'game changer': 'game-changer',
        'um actually': 'um-actually',
        'breaking news': 'breaking-news',
        'rats rent a shop': 'rats-rent-a-shop',
        'very important people': 'very-important-people',
        'make some noise': 'make-some-noise',
        'total forgiveness': 'total-forgiveness',
        'adventuring party': 'adventuring-party',
        'dirty laundry': 'dirty-laundry',
    }
    
    title_lower = title.lower()
    for show_key, show_slug in known_shows.items():
        if show_key in title_lower:
            return show_slug
    
    # Default: use first part of title before any delimiter
    first_part = re.split(r'[:\-\|\[\]]', title)[0].strip()
    return normalize_show_name(first_part) if first_part else 'unknown-show'


def normalize_show_name(show_name: str) -> str:
    """
    Normalize show name to a URL-friendly slug.
    
    Args:
        show_name: Raw show name
        
    Returns:
        Normalized show name (lowercase, hyphenated)
    """
    # Convert to lowercase and replace spaces with hyphens
    normalized = show_name.lower().strip()
    # Remove special characters except hyphens and alphanumeric
    normalized = re.sub(r'[^a-z0-9\s-]', '', normalized)
    # Replace spaces with hyphens
    normalized = re.sub(r'\s+', '-', normalized)
    # Remove consecutive hyphens
    normalized = re.sub(r'-+', '-', normalized)
    # Remove leading/trailing hyphens
    normalized = normalized.strip('-')
    
    return normalized or 'unknown-show'


def group_episodes_by_show(episodes: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group episodes by their show name.
    
    Args:
        episodes: List of episode dictionaries
        
    Returns:
        Dictionary mapping show names to lists of episodes
    """
    shows = {}
    
    for episode in episodes:
        show_name = episode.get('show_name', 'unknown-show')
        if show_name not in shows:
            shows[show_name] = []
        shows[show_name].append(episode)
    
    return shows
