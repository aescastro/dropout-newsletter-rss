"""
Utility functions for the transformer
"""

import os
from pathlib import Path


def ensure_directory(directory: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Path to the directory
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


def get_env_variable(var_name: str, default: str = "") -> str:
    """
    Get an environment variable with a default value.
    
    Args:
        var_name: Name of the environment variable
        default: Default value if variable is not set
        
    Returns:
        Value of the environment variable or default
    """
    return os.getenv(var_name, default)
