"""
Config module - Configuration management and settings.

This module handles:
- User preferences and interests
- System prompts and templates
- Environment variable management
- Configuration validation
"""

from .config_parser import (
    ConfigParser,
    ThinkleConfig,
    NewsletterSettings,
    ContentSettings,
    RedditSettings,
    YouTubeSettings,
    OutputSettings,
    load_config,
)

__all__ = [
    'ConfigParser',
    'ThinkleConfig',
    'NewsletterSettings',
    'ContentSettings',
    'RedditSettings',
    'YouTubeSettings',
    'OutputSettings',
    'load_config',
]
