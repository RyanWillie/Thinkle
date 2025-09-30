#!/usr/bin/env python3
"""
Configuration parser for TheThinkle.ai newsletter system.

This module provides functionality to parse, validate, and manage
configuration settings from the interests.yaml file using Pydantic.
"""

import yaml
from typing import Dict, List, Any, Optional, Union, Literal
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, model_validator


class RedditSettings(BaseModel):
    """Reddit-specific configuration settings."""
    min_upvotes: int = Field(default=100, ge=0, description="Minimum upvotes for consideration")
    max_age_hours: int = Field(default=48, gt=0, description="Maximum age in hours for posts")


class YouTubeSettings(BaseModel):
    """YouTube-specific configuration settings."""
    min_views: int = Field(default=10000, ge=0, description="Minimum views for consideration")
    max_duration_minutes: int = Field(default=60, gt=0, description="Maximum video duration in minutes")


class ContentSettings(BaseModel):
    """Content preferences configuration."""
    include_academic: bool = Field(default=True, description="Include ArXiv papers")
    include_reddit: bool = Field(default=True, description="Include Reddit discussions")
    include_youtube: bool = Field(default=True, description="Include YouTube content")
    include_news: bool = Field(default=True, description="Include news articles")
    reddit: RedditSettings = Field(default_factory=RedditSettings)
    youtube: YouTubeSettings = Field(default_factory=YouTubeSettings)
    
    @model_validator(mode='after')
    def validate_at_least_one_source(self):
        """Ensure at least one content source is enabled."""
        sources = [
            self.include_academic,
            self.include_reddit,
            self.include_youtube,
            self.include_news
        ]
        if not any(sources):
            raise ValueError("At least one content source must be enabled")
        return self


class NewsletterSettings(BaseModel):
    """Newsletter preferences configuration."""
    tone: Literal["professional", "witty", "casual", "academic"] = Field(
        default="witty", 
        description="Newsletter tone"
    )
    include_opinions: bool = Field(default=True, description="Include AI-generated opinions")
    frequency: Literal["daily", "weekly"] = Field(default="weekly", description="Newsletter frequency")
    max_stories: int = Field(default=10, gt=0, le=50, description="Maximum stories per newsletter")


class OutputSettings(BaseModel):
    """Output preferences configuration."""
    format: Literal["markdown", "pdf", "html"] = Field(
        default="markdown", 
        description="Output format"
    )
    include_sources: bool = Field(default=True, description="Include source links")
    include_summary_stats: bool = Field(default=True, description="Include reading statistics")


class ModelSettings(BaseModel):
    """Model names per agent."""
    planner: str = Field(default="gpt-5-mini", description="Planner LLM model name")
    scout: str = Field(default="gpt-5-mini", description="Scout LLM model name")
    evaluator: str = Field(default="gpt-5-mini", description="Evaluator LLM model name")
    writer: str = Field(default="gpt-5-mini", description="Writer LLM model name")


class ThinkleConfig(BaseModel):
    """Main configuration class for TheThinkle.ai."""
    interests: List[str] = Field(
        min_length=1,
        description="List of topics to follow"
    )
    user_profile: str = Field(
        default="",
        description="Short background on the user to tailor content"
    )
    newsletter: NewsletterSettings = Field(default_factory=NewsletterSettings)
    content: ContentSettings = Field(default_factory=ContentSettings)
    output: OutputSettings = Field(default_factory=OutputSettings)
    models: ModelSettings = Field(default_factory=ModelSettings)
    max_tasks: int = Field(default=1, gt=0, le=10, description="Maximum number of tasks to generate")
    @field_validator('interests')
    @classmethod
    def validate_interests(cls, v):
        """Validate interests list."""
        if not v:
            raise ValueError("At least one interest must be specified")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_interests = []
        for interest in v:
            if interest.lower() not in seen:
                seen.add(interest.lower())
                unique_interests.append(interest.strip())
        
        return unique_interests
    
    model_config = {
        "extra": "forbid",  # Don't allow extra fields
        "validate_assignment": True,  # Validate on assignment
        "use_enum_values": True
    }


class ConfigParser:
    """
    Configuration parser for TheThinkle.ai newsletter system.
    
    Handles loading, parsing, and validation of YAML configuration files using Pydantic.
    """
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize the config parser.
        
        Args:
            config_path: Path to the configuration file. If None, defaults to
                        config/interests.yaml in the project root.
        """
        if config_path is None:
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "interests.yaml"
        
        self.config_path = Path(config_path)
        self._config: Optional[ThinkleConfig] = None
    
    def load_config(self) -> ThinkleConfig:
        """
        Load and parse the configuration file.
        
        Returns:
            ThinkleConfig: Parsed and validated configuration object.
            
        Raises:
            FileNotFoundError: If the configuration file doesn't exist.
            yaml.YAMLError: If the YAML file is malformed.
            ValidationError: If the configuration contains invalid values.
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                raw_config = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to parse YAML configuration: {e}")
        
        if raw_config is None:
            raise ValueError("Configuration file is empty")
        
        # Parse and validate configuration using Pydantic
        try:
            config = ThinkleConfig(**raw_config)
        except Exception as e:
            raise ValueError(f"Configuration validation failed: {e}")
        
        self._config = config
        return config
    
    def get_config(self) -> ThinkleConfig:
        """
        Get the loaded configuration.
        
        Returns:
            ThinkleConfig: The loaded configuration object.
            
        Raises:
            RuntimeError: If configuration hasn't been loaded yet.
        """
        if self._config is None:
            raise RuntimeError("Configuration not loaded. Call load_config() first.")
        return self._config
    
    def reload_config(self) -> ThinkleConfig:
        """
        Reload the configuration from file.
        
        Returns:
            ThinkleConfig: Freshly loaded configuration object.
        """
        return self.load_config()
    
    def save_config(self, config: ThinkleConfig, output_path: Optional[Union[str, Path]] = None) -> None:
        """
        Save configuration to YAML file.
        
        Args:
            config: Configuration object to save.
            output_path: Path to save the configuration. If None, uses the original config path.
        """
        if output_path is None:
            output_path = self.config_path
        else:
            output_path = Path(output_path)
        
        # Convert Pydantic model to dictionary
        config_dict = config.model_dump()
        
        with open(output_path, 'w', encoding='utf-8') as file:
            yaml.dump(config_dict, file, default_flow_style=False, sort_keys=False, indent=2)
    
    def create_example_config(self, output_path: Optional[Union[str, Path]] = None) -> ThinkleConfig:
        """
        Create an example configuration file with default values.
        
        Args:
            output_path: Path to save the example configuration.
            
        Returns:
            ThinkleConfig: Example configuration object.
        """
        example_config = ThinkleConfig(
            interests=[
                "artificial intelligence",
                "machine learning", 
                "technology trends",
                "climate change"
            ]
        )
        
        if output_path:
            self.save_config(example_config, output_path)
        
        return example_config


def load_config(config_path: Optional[Union[str, Path]] = None) -> ThinkleConfig:
    """
    Convenience function to load configuration.
    
    Args:
        config_path: Path to the configuration file.
        
    Returns:
        ThinkleConfig: Loaded configuration object.
    """
    parser = ConfigParser(config_path)
    return parser.load_config()


# Example usage
if __name__ == "__main__":
    # Load and display configuration
    try:
        config = load_config()
        print("Configuration loaded successfully!")
        print(f"Interests: {config.interests}")
        print(f"Newsletter tone: {config.newsletter.tone}")
        print(f"Max stories: {config.newsletter.max_stories}")
        print(f"Output format: {config.output.format}")
        
        # Demonstrate Pydantic features
        print("\n--- Pydantic Features ---")
        print("Configuration as JSON:")
        print(config.model_dump_json(indent=2))
        
        print("\nConfiguration schema:")
        import json
        print(json.dumps(config.model_json_schema(), indent=2))
        
    except Exception as e:
        print(f"Error loading configuration: {e}")
