"""
Unit tests for the configuration parser module.

Tests cover Pydantic model validation, YAML parsing, configuration loading,
and all validation scenarios.
"""

import pytest
import yaml
import tempfile
from pathlib import Path
from pydantic import ValidationError
from unittest.mock import patch, mock_open

from config import (
    ConfigParser, 
    ThinkleConfig, 
    NewsletterSettings,
    ContentSettings,
    RedditSettings,
    YouTubeSettings,
    OutputSettings,
    load_config
)
from tests.fixtures.sample_configs import (
    VALID_MINIMAL_CONFIG,
    VALID_FULL_CONFIG,
    VALID_ALTERNATIVE_CONFIG,
    INVALID_EMPTY_INTERESTS,
    INVALID_MISSING_INTERESTS,
    INVALID_TONE,
    INVALID_FREQUENCY,
    INVALID_FORMAT,
    INVALID_NEGATIVE_VALUES,
    INVALID_ZERO_VALUES,
    INVALID_ALL_SOURCES_DISABLED,
    INVALID_EXTRA_FIELDS,
    DUPLICATE_INTERESTS,
    WHITESPACE_INTERESTS,
    BOUNDARY_VALUES,
    ACADEMIC_FOCUSED_CONFIG,
    SOCIAL_FOCUSED_CONFIG
)


class TestThinkleConfig:
    """Test the main ThinkleConfig Pydantic model."""

    def test_valid_minimal_config(self):
        """Test creating config with minimal valid data."""
        config = ThinkleConfig(**VALID_MINIMAL_CONFIG)
        assert config.interests == ["artificial intelligence"]
        assert config.newsletter.tone == "witty"  # default
        assert config.newsletter.max_stories == 10  # default
        assert config.content.include_academic is True  # default

    def test_valid_full_config(self):
        """Test creating config with all fields specified."""
        config = ThinkleConfig(**VALID_FULL_CONFIG)
        assert len(config.interests) == 7
        assert config.newsletter.tone == "witty"
        assert config.newsletter.max_stories == 10
        assert config.content.reddit.min_upvotes == 100
        assert config.output.format == "markdown"

    def test_valid_alternative_config(self):
        """Test alternative valid configuration values."""
        config = ThinkleConfig(**VALID_ALTERNATIVE_CONFIG)
        assert config.newsletter.tone == "professional"
        assert config.newsletter.frequency == "daily"
        assert config.newsletter.include_opinions is False
        assert config.output.format == "html"

    def test_empty_interests_validation(self):
        """Test that empty interests list is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ThinkleConfig(**INVALID_EMPTY_INTERESTS)
        
        errors = exc_info.value.errors()
        assert any("at least 1 item" in str(error["msg"]).lower() for error in errors)

    def test_missing_interests_validation(self):
        """Test that missing interests field is rejected."""
        # Now that interests is required (no default), missing interests should fail
        with pytest.raises(ValidationError) as exc_info:
            ThinkleConfig(**INVALID_MISSING_INTERESTS)
        
        errors = exc_info.value.errors()
        assert any("interests" in str(error["loc"]) for error in errors)

    def test_invalid_tone_validation(self):
        """Test that invalid newsletter tone is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ThinkleConfig(**INVALID_TONE)
        
        errors = exc_info.value.errors()
        assert any("tone" in str(error["loc"]) for error in errors)

    def test_invalid_frequency_validation(self):
        """Test that invalid newsletter frequency is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ThinkleConfig(**INVALID_FREQUENCY)
        
        errors = exc_info.value.errors()
        assert any("frequency" in str(error["loc"]) for error in errors)

    def test_invalid_format_validation(self):
        """Test that invalid output format is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ThinkleConfig(**INVALID_FORMAT)
        
        errors = exc_info.value.errors()
        assert any("format" in str(error["loc"]) for error in errors)

    def test_negative_values_validation(self):
        """Test that negative values are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ThinkleConfig(**INVALID_NEGATIVE_VALUES)
        
        errors = exc_info.value.errors()
        # Should have multiple validation errors for negative values
        assert len(errors) > 1

    def test_zero_values_validation(self):
        """Test that zero values are rejected where appropriate."""
        with pytest.raises(ValidationError) as exc_info:
            ThinkleConfig(**INVALID_ZERO_VALUES)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0

    def test_all_sources_disabled_validation(self):
        """Test that having all content sources disabled is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ThinkleConfig(**INVALID_ALL_SOURCES_DISABLED)
        
        errors = exc_info.value.errors()
        assert any("at least one content source" in str(error["msg"]).lower() for error in errors)

    def test_extra_fields_validation(self):
        """Test that extra fields are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ThinkleConfig(**INVALID_EXTRA_FIELDS)
        
        errors = exc_info.value.errors()
        assert any("extra" in str(error["msg"]).lower() for error in errors)

    def test_duplicate_interests_handling(self):
        """Test that duplicate interests are properly handled."""
        config = ThinkleConfig(**DUPLICATE_INTERESTS)
        
        # Should remove duplicates while preserving order
        assert len(config.interests) < len(DUPLICATE_INTERESTS["interests"])
        assert "AI" in config.interests
        assert "Machine Learning" in config.interests

    def test_whitespace_interests_handling(self):
        """Test that whitespace in interests is properly handled."""
        config = ThinkleConfig(**WHITESPACE_INTERESTS)
        
        # Should strip whitespace
        for interest in config.interests:
            assert interest == interest.strip()
            assert "\t" not in interest
            assert "\n" not in interest

    def test_boundary_values(self):
        """Test boundary values for numeric fields."""
        config = ThinkleConfig(**BOUNDARY_VALUES)
        assert config.newsletter.max_stories == 50
        assert config.content.reddit.min_upvotes == 0
        assert config.content.reddit.max_age_hours == 1

    def test_model_dump_json(self):
        """Test JSON serialization."""
        config = ThinkleConfig(**VALID_FULL_CONFIG)
        json_str = config.model_dump_json()
        assert isinstance(json_str, str)
        assert "interests" in json_str
        assert "newsletter" in json_str

    def test_model_dump(self):
        """Test dictionary serialization."""
        config = ThinkleConfig(**VALID_FULL_CONFIG)
        config_dict = config.model_dump()
        assert isinstance(config_dict, dict)
        assert "interests" in config_dict
        assert "newsletter" in config_dict

    def test_model_json_schema(self):
        """Test JSON schema generation."""
        schema = ThinkleConfig.model_json_schema()
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "interests" in schema["properties"]


class TestNewsletterSettings:
    """Test NewsletterSettings Pydantic model."""

    def test_valid_settings(self):
        """Test valid newsletter settings."""
        settings = NewsletterSettings(
            tone="professional",
            include_opinions=False,
            frequency="daily",
            max_stories=5
        )
        assert settings.tone == "professional"
        assert settings.include_opinions is False
        assert settings.frequency == "daily"
        assert settings.max_stories == 5

    def test_default_values(self):
        """Test default values."""
        settings = NewsletterSettings()
        assert settings.tone == "witty"
        assert settings.include_opinions is True
        assert settings.frequency == "weekly"
        assert settings.max_stories == 10

    def test_max_stories_validation(self):
        """Test max_stories validation."""
        # Test upper bound
        with pytest.raises(ValidationError):
            NewsletterSettings(max_stories=100)  # Above limit
        
        # Test lower bound
        with pytest.raises(ValidationError):
            NewsletterSettings(max_stories=0)  # Zero not allowed


class TestContentSettings:
    """Test ContentSettings Pydantic model."""

    def test_valid_settings(self):
        """Test valid content settings."""
        settings = ContentSettings(
            include_academic=False,
            include_reddit=True,
            include_youtube=True,
            include_news=False
        )
        assert settings.include_academic is False
        assert settings.include_reddit is True

    def test_at_least_one_source_validation(self):
        """Test that at least one source must be enabled."""
        with pytest.raises(ValidationError) as exc_info:
            ContentSettings(
                include_academic=False,
                include_reddit=False,
                include_youtube=False,
                include_news=False
            )
        
        errors = exc_info.value.errors()
        assert any("at least one content source" in str(error["msg"]).lower() for error in errors)

    def test_nested_settings(self):
        """Test nested Reddit and YouTube settings."""
        settings = ContentSettings()
        assert isinstance(settings.reddit, RedditSettings)
        assert isinstance(settings.youtube, YouTubeSettings)
        assert settings.reddit.min_upvotes == 100  # default


class TestConfigParser:
    """Test the ConfigParser class."""

    def test_init_with_default_path(self):
        """Test initialization with default config path."""
        parser = ConfigParser()
        assert parser.config_path.name == "interests.yaml"

    def test_init_with_custom_path(self, temp_config_file):
        """Test initialization with custom config path."""
        parser = ConfigParser(temp_config_file)
        assert parser.config_path == temp_config_file

    def test_load_config_success(self, temp_config_file):
        """Test successful config loading."""
        parser = ConfigParser(temp_config_file)
        config = parser.load_config()
        
        assert isinstance(config, ThinkleConfig)
        assert len(config.interests) > 0
        assert parser._config is not None

    def test_load_config_file_not_found(self):
        """Test loading config when file doesn't exist."""
        parser = ConfigParser("/nonexistent/path/config.yaml")
        
        with pytest.raises(FileNotFoundError):
            parser.load_config()

    def test_load_config_invalid_yaml(self, temp_dir):
        """Test loading config with invalid YAML."""
        invalid_yaml_file = temp_dir / "invalid.yaml"
        with open(invalid_yaml_file, 'w') as f:
            f.write("invalid: yaml: content: [")
        
        parser = ConfigParser(invalid_yaml_file)
        with pytest.raises(yaml.YAMLError):
            parser.load_config()

    def test_load_config_empty_file(self, temp_dir):
        """Test loading empty config file."""
        empty_file = temp_dir / "empty.yaml"
        empty_file.touch()
        
        parser = ConfigParser(empty_file)
        with pytest.raises(ValueError, match="empty"):
            parser.load_config()

    def test_load_config_validation_error(self, temp_dir):
        """Test loading config with validation errors."""
        invalid_config_file = temp_dir / "invalid_config.yaml"
        with open(invalid_config_file, 'w') as f:
            yaml.dump(INVALID_TONE, f)
        
        parser = ConfigParser(invalid_config_file)
        with pytest.raises(ValueError, match="validation failed"):
            parser.load_config()

    def test_get_config_success(self, config_parser):
        """Test getting loaded config."""
        config_parser.load_config()
        config = config_parser.get_config()
        
        assert isinstance(config, ThinkleConfig)

    def test_get_config_not_loaded(self):
        """Test getting config when not loaded."""
        parser = ConfigParser()
        
        with pytest.raises(RuntimeError, match="not loaded"):
            parser.get_config()

    def test_reload_config(self, config_parser):
        """Test reloading config."""
        config1 = config_parser.load_config()
        config2 = config_parser.reload_config()
        
        assert config1.model_dump() == config2.model_dump()

    def test_save_config(self, config_parser, temp_dir):
        """Test saving config to file."""
        config = config_parser.load_config()
        output_file = temp_dir / "saved_config.yaml"
        
        config_parser.save_config(config, output_file)
        
        assert output_file.exists()
        
        # Verify saved content can be loaded
        saved_parser = ConfigParser(output_file)
        saved_config = saved_parser.load_config()
        
        assert saved_config.model_dump() == config.model_dump()

    def test_save_config_default_path(self, config_parser):
        """Test saving config to default path."""
        config = config_parser.load_config()
        
        # Should not raise an error
        config_parser.save_config(config)

    def test_create_example_config(self, temp_dir):
        """Test creating example config."""
        parser = ConfigParser()
        output_file = temp_dir / "example_config.yaml"
        
        config = parser.create_example_config(output_file)
        
        assert isinstance(config, ThinkleConfig)
        assert output_file.exists()
        assert len(config.interests) > 0


class TestLoadConfigFunction:
    """Test the load_config convenience function."""

    def test_load_config_default_path(self):
        """Test load_config with default path."""
        with patch.object(ConfigParser, 'load_config') as mock_load:
            mock_config = ThinkleConfig(interests=["test"])
            mock_load.return_value = mock_config
            
            result = load_config()
            
            assert result == mock_config
            mock_load.assert_called_once()

    def test_load_config_custom_path(self, temp_config_file):
        """Test load_config with custom path."""
        config = load_config(temp_config_file)
        
        assert isinstance(config, ThinkleConfig)
        assert len(config.interests) > 0


class TestSpecialConfigurations:
    """Test special configuration scenarios."""

    def test_academic_focused_config(self):
        """Test academic-focused configuration."""
        config = ThinkleConfig(**ACADEMIC_FOCUSED_CONFIG)
        
        assert config.newsletter.tone == "academic"
        assert config.newsletter.include_opinions is False
        assert config.content.include_academic is True
        assert config.content.include_reddit is False

    def test_social_focused_config(self):
        """Test social-focused configuration."""
        config = ThinkleConfig(**SOCIAL_FOCUSED_CONFIG)
        
        assert config.newsletter.tone == "casual"
        assert config.newsletter.frequency == "daily"
        assert config.content.include_reddit is True
        assert config.content.reddit.min_upvotes == 500

    @pytest.mark.parametrize("tone", ["professional", "witty", "casual", "academic"])
    def test_all_valid_tones(self, tone):
        """Test all valid tone values."""
        config = ThinkleConfig(
            interests=["test"],
            newsletter=NewsletterSettings(tone=tone)
        )
        assert config.newsletter.tone == tone

    @pytest.mark.parametrize("frequency", ["daily", "weekly"])
    def test_all_valid_frequencies(self, frequency):
        """Test all valid frequency values."""
        config = ThinkleConfig(
            interests=["test"],
            newsletter=NewsletterSettings(frequency=frequency)
        )
        assert config.newsletter.frequency == frequency

    @pytest.mark.parametrize("format_type", ["markdown", "pdf", "html"])
    def test_all_valid_formats(self, format_type):
        """Test all valid output formats."""
        config = ThinkleConfig(
            interests=["test"],
            output=OutputSettings(format=format_type)
        )
        assert config.output.format == format_type
