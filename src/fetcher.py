"""
Fetcher module for retrieving the Kill The Newsletter RSS feed
"""

import requests
from typing import Optional


def fetch_feed(url: str) -> Optional[str]:
    """
    Fetch the RSS feed content from the given URL.
    
    Args:
        url: The Kill The Newsletter RSS feed URL
        
    Returns:
        The raw RSS feed XML content as a string, or None if fetch fails
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching feed from {url}: {e}")
        return None
