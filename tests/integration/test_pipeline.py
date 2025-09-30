"""
Integration tests for the newsletter generation pipeline.

These tests verify that components work together correctly
and that the full pipeline can be executed successfully.
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path

from config import load_config, ConfigParser


class TestPipelineIntegration:
    """Test integration between pipeline components."""

    @pytest.mark.integration
    def test_config_loading_in_pipeline(self):
        """Test that config can be loaded in pipeline context."""
        # This test will be expanded as more components are added
        config = load_config()
        
        assert config is not None
        assert len(config.interests) > 0
        assert config.newsletter.tone in ["professional", "witty", "casual", "academic"]

    @pytest.mark.integration
    def test_config_validation_in_pipeline(self):
        """Test config validation in pipeline context."""
        parser = ConfigParser()
        config = parser.load_config()
        
        # Verify all required components are valid
        assert config.interests
        assert config.newsletter
        assert config.content
        assert config.output
        
        # Verify at least one content source is enabled
        sources = [
            config.content.include_academic,
            config.content.include_reddit,
            config.content.include_youtube,
            config.content.include_news
        ]
        assert any(sources)

    @pytest.mark.integration
    @pytest.mark.slow
    def test_end_to_end_config_flow(self, temp_dir):
        """Test complete config flow from file to processing."""
        # Create a test config
        test_config_data = {
            "interests": ["artificial intelligence", "space exploration"],
            "newsletter": {
                "tone": "professional",
                "frequency": "weekly",
                "max_stories": 5
            },
            "content": {
                "include_academic": True,
                "include_reddit": False,
                "include_youtube": True,
                "include_news": True
            },
            "output": {
                "format": "markdown",
                "include_sources": True
            }
        }
        
        # Save to file
        import yaml
        config_file = temp_dir / "test_pipeline_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(test_config_data, f)
        
        # Load and process
        parser = ConfigParser(config_file)
        config = parser.load_config()
        
        # Verify processing would work
        assert config.interests == ["artificial intelligence", "space exploration"]
        assert config.newsletter.tone == "professional"
        assert config.content.include_academic is True
        assert config.content.include_reddit is False
        
        # Test config modification and save
        config.newsletter.max_stories = 8
        parser.save_config(config, temp_dir / "modified_config.yaml")
        
        # Verify modification persisted
        modified_parser = ConfigParser(temp_dir / "modified_config.yaml")
        modified_config = modified_parser.load_config()
        assert modified_config.newsletter.max_stories == 8


class TestComponentIntegration:
    """Test integration between specific components."""

    @pytest.mark.integration
    def test_config_with_mock_agents(self, sample_config):
        """Test config integration with mock agents."""
        # This will be expanded as agent components are added
        with patch('agents.planner.PlannerAgent') as mock_planner:
            mock_planner.return_value.plan.return_value = {"status": "success"}
            
            # Config should provide necessary settings for agents
            assert sample_config.interests
            assert sample_config.newsletter.tone
            
            # Mock agent should be configurable with our settings
            mock_planner.assert_not_called()  # Not called yet, but available

    @pytest.mark.integration
    def test_config_with_mock_tools(self, sample_config):
        """Test config integration with mock tools."""
        # This will be expanded as tool components are added
        with patch('tools.basic_tools.RedditTool') as mock_reddit:
            mock_reddit.return_value.fetch.return_value = []
            
            # Config should provide tool settings
            assert sample_config.content.reddit.min_upvotes >= 0
            assert sample_config.content.reddit.max_age_hours > 0
            
            # Mock tool configuration
            if sample_config.content.include_reddit:
                # Tool would be configured with these settings
                assert sample_config.content.reddit.min_upvotes == 100

    @pytest.mark.integration
    def test_config_serialization_roundtrip(self, sample_config, temp_dir):
        """Test config can survive serialization roundtrips."""
        # JSON roundtrip
        json_str = sample_config.model_dump_json()
        from config import ThinkleConfig
        config_from_json = ThinkleConfig.model_validate_json(json_str)
        
        assert config_from_json.model_dump() == sample_config.model_dump()
        
        # YAML roundtrip
        import yaml
        yaml_file = temp_dir / "roundtrip.yaml"
        with open(yaml_file, 'w') as f:
            yaml.dump(sample_config.model_dump(), f)
        
        with open(yaml_file, 'r') as f:
            yaml_data = yaml.safe_load(f)
        
        config_from_yaml = ThinkleConfig(**yaml_data)
        assert config_from_yaml.model_dump() == sample_config.model_dump()


class TestErrorHandling:
    """Test error handling in integration scenarios."""

    @pytest.mark.integration
    def test_graceful_config_error_handling(self):
        """Test that config errors are handled gracefully."""
        # Test with non-existent file
        parser = ConfigParser("/nonexistent/config.yaml")
        
        with pytest.raises(FileNotFoundError):
            parser.load_config()
        
        # Should not crash the application
        assert parser._config is None

    @pytest.mark.integration
    def test_partial_config_recovery(self, temp_dir):
        """Test recovery from partial config errors."""
        # Create config with some invalid data
        partial_config = {
            "interests": ["ai"],
            "newsletter": {
                "tone": "witty",
                "max_stories": "invalid"  # Wrong type
            }
        }
        
        import yaml
        config_file = temp_dir / "partial_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(partial_config, f)
        
        parser = ConfigParser(config_file)
        
        with pytest.raises(ValueError):
            parser.load_config()
        
        # Parser should still be usable for other operations
        example_config = parser.create_example_config()
        assert example_config is not None
