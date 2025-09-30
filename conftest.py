"""
Global pytest configuration and fixtures for TheThinkle.ai tests.

This module provides shared fixtures and configuration that can be used
across all test modules.
"""

import os
import tempfile
import pytest
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock, patch

# Add the project root to Python path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from config import ThinkleConfig, ConfigParser


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent


@pytest.fixture(scope="session") 
def test_data_dir(project_root) -> Path:
    """Get the test data directory."""
    return project_root / "tests" / "fixtures"


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_config_data() -> Dict[str, Any]:
    """Sample configuration data for testing."""
    return {
        "interests": [
            "artificial intelligence",
            "machine learning",
            "technology"
        ],
        "newsletter": {
            "tone": "witty",
            "include_opinions": True,
            "frequency": "weekly",
            "max_stories": 10
        },
        "content": {
            "include_academic": True,
            "include_reddit": True,
            "include_youtube": True,
            "include_news": True,
            "reddit": {
                "min_upvotes": 100,
                "max_age_hours": 48
            },
            "youtube": {
                "min_views": 10000,
                "max_duration_minutes": 60
            }
        },
        "output": {
            "format": "markdown",
            "include_sources": True,
            "include_summary_stats": True
        }
    }


@pytest.fixture
def sample_config(sample_config_data) -> ThinkleConfig:
    """Create a sample ThinkleConfig instance."""
    return ThinkleConfig(**sample_config_data)


@pytest.fixture
def temp_config_file(temp_dir, sample_config_data):
    """Create a temporary config file with sample data."""
    import yaml
    
    config_file = temp_dir / "test_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(sample_config_data, f, default_flow_style=False, indent=2)
    
    return config_file


@pytest.fixture
def config_parser(temp_config_file) -> ConfigParser:
    """Create a ConfigParser instance with a temporary config file."""
    return ConfigParser(config_path=temp_config_file)


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    with patch('openai.OpenAI') as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_reddit_client():
    """Mock Reddit client for testing."""
    with patch('praw.Reddit') as mock_reddit:
        mock_instance = Mock()
        mock_reddit.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_youtube_client():
    """Mock YouTube client for testing."""
    with patch('youtube_transcript_api.YouTubeTranscriptApi') as mock_youtube:
        yield mock_youtube


@pytest.fixture
def mock_requests():
    """Mock requests library for HTTP calls."""
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_response.text = "Mock response text"
        
        mock_get.return_value = mock_response
        mock_post.return_value = mock_response
        
        yield {
            'get': mock_get,
            'post': mock_post,
            'response': mock_response
        }


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    # Set test environment variables
    os.environ['TESTING'] = 'true'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    
    yield
    
    # Clean up
    if 'TESTING' in os.environ:
        del os.environ['TESTING']
    if 'LOG_LEVEL' in os.environ:
        del os.environ['LOG_LEVEL']


@pytest.fixture
def disable_external_apis():
    """Disable external API calls during testing."""
    with patch.dict(os.environ, {'DISABLE_EXTERNAL_APIS': 'true'}):
        yield


# Pytest hooks
def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Auto-mark tests based on file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Auto-mark slow tests
        if "slow" in item.name or "integration" in str(item.fspath):
            item.add_marker(pytest.mark.slow)
