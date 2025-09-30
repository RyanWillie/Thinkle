"""
Test utilities and helper functions.

This module provides utility functions and classes to make testing
easier and more consistent across the test suite.
"""

import yaml
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from unittest.mock import Mock, MagicMock
from contextlib import contextmanager

from config import ThinkleConfig, ConfigParser


class ConfigTestHelper:
    """Helper class for testing configuration-related functionality."""

    @staticmethod
    def create_temp_config(config_data: Dict[str, Any], suffix: str = ".yaml") -> Path:
        """Create a temporary config file with given data."""
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False)
        temp_path = Path(temp_file.name)

        with open(temp_path, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False, indent=2)

        return temp_path

    @staticmethod
    def create_invalid_yaml_file(content: str) -> Path:
        """Create a temporary file with invalid YAML content."""
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
        temp_path = Path(temp_file.name)

        with open(temp_path, "w") as f:
            f.write(content)

        return temp_path

    @staticmethod
    def assert_config_equals(config1: ThinkleConfig, config2: ThinkleConfig):
        """Assert that two configs are equal."""
        assert config1.model_dump() == config2.model_dump()

    @staticmethod
    def create_minimal_valid_config() -> Dict[str, Any]:
        """Create minimal valid config data."""
        return {"interests": ["artificial intelligence"]}

    @staticmethod
    def create_maximal_valid_config() -> Dict[str, Any]:
        """Create config with all possible valid fields."""
        return {
            "interests": [
                "artificial intelligence",
                "machine learning",
                "quantum computing",
                "space exploration",
                "biotechnology",
            ],
            "newsletter": {
                "tone": "academic",
                "include_opinions": False,
                "frequency": "daily",
                "max_stories": 50,
            },
            "content": {
                "include_academic": True,
                "include_reddit": True,
                "include_youtube": True,
                "include_news": True,
                "reddit": {"min_upvotes": 1000, "max_age_hours": 12},
                "youtube": {"min_views": 100000, "max_duration_minutes": 30},
            },
            "output": {
                "format": "pdf",
                "include_sources": False,
                "include_summary_stats": False,
            },
        }


class MockHelper:
    """Helper class for creating mocks and test doubles."""

    @staticmethod
    def create_mock_reddit_response(posts_count: int = 3) -> Mock:
        """Create a mock Reddit API response."""
        mock_response = Mock()
        mock_posts = []

        for i in range(posts_count):
            mock_post = Mock()
            mock_post.title = f"Test Post {i+1}"
            mock_post.selftext = f"This is test post content {i+1}"
            mock_post.score = 100 * (i + 1)
            mock_post.num_comments = 10 * (i + 1)
            mock_post.url = f"https://reddit.com/post/{i+1}"
            mock_post.subreddit.display_name = "technology"
            mock_posts.append(mock_post)

        mock_response.posts = mock_posts
        return mock_response

    @staticmethod
    def create_mock_youtube_response(videos_count: int = 2) -> Mock:
        """Create a mock YouTube API response."""
        mock_response = Mock()
        mock_videos = []

        for i in range(videos_count):
            mock_video = Mock()
            mock_video.title = f"Test Video {i+1}"
            mock_video.description = f"This is test video description {i+1}"
            mock_video.view_count = 10000 * (i + 1)
            mock_video.duration = "PT15M30S"
            mock_video.video_id = f"test_video_{i+1}"
            mock_videos.append(mock_video)

        mock_response.videos = mock_videos
        return mock_response

    @staticmethod
    def create_mock_openai_response(content: str = "Mock AI response") -> Mock:
        """Create a mock OpenAI API response."""
        mock_response = Mock()
        mock_choice = Mock()
        mock_choice.message.content = content
        mock_response.choices = [mock_choice]
        mock_response.usage.total_tokens = 150
        return mock_response


class ValidationTestHelper:
    """Helper class for testing validation scenarios."""

    @staticmethod
    def create_validation_test_cases():
        """Create a comprehensive set of validation test cases."""
        return {
            "empty_interests": {
                "data": {"interests": []},
                "should_fail": True,
                "error_contains": "at least 1 item",
            },
            "invalid_tone": {
                "data": {"interests": ["ai"], "newsletter": {"tone": "invalid"}},
                "should_fail": True,
                "error_contains": "tone",
            },
            "negative_max_stories": {
                "data": {"interests": ["ai"], "newsletter": {"max_stories": -1}},
                "should_fail": True,
                "error_contains": "greater than 0",
            },
            "excessive_max_stories": {
                "data": {"interests": ["ai"], "newsletter": {"max_stories": 100}},
                "should_fail": True,
                "error_contains": "less than or equal to 50",
            },
            "all_sources_disabled": {
                "data": {
                    "interests": ["ai"],
                    "content": {
                        "include_academic": False,
                        "include_reddit": False,
                        "include_youtube": False,
                        "include_news": False,
                    },
                },
                "should_fail": True,
                "error_contains": "at least one content source",
            },
        }

    @staticmethod
    def run_validation_test(test_name: str, test_case: Dict[str, Any]):
        """Run a single validation test case."""
        from pydantic import ValidationError

        try:
            config = ThinkleConfig(**test_case["data"])
            if test_case["should_fail"]:
                raise AssertionError(f"Test {test_name} should have failed but didn't")
            return True, config
        except ValidationError as e:
            if not test_case["should_fail"]:
                raise AssertionError(f"Test {test_name} should not have failed: {e}")

            error_msg = str(e)
            if test_case["error_contains"] not in error_msg.lower():
                raise AssertionError(
                    f"Test {test_name} error message doesn't contain '{test_case['error_contains']}': {error_msg}"
                )
            return False, str(e)


@contextmanager
def temporary_config_file(config_data: Dict[str, Any]):
    """Context manager for temporary config files."""
    temp_path = ConfigTestHelper.create_temp_config(config_data)
    try:
        yield temp_path
    finally:
        if temp_path.exists():
            temp_path.unlink()


@contextmanager
def mock_external_apis():
    """Context manager to mock all external API calls."""
    from unittest.mock import patch

    with patch("praw.Reddit") as mock_reddit, patch(
        "openai.OpenAI"
    ) as mock_openai, patch(
        "youtube_transcript_api.YouTubeTranscriptApi"
    ) as mock_youtube, patch(
        "requests.get"
    ) as mock_requests:

        # Configure mocks
        mock_reddit.return_value = MockHelper.create_mock_reddit_response()
        mock_openai.return_value.chat.completions.create.return_value = (
            MockHelper.create_mock_openai_response()
        )
        mock_youtube.get_transcript.return_value = [
            {"text": "Mock transcript", "start": 0.0}
        ]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_requests.return_value = mock_response

        yield {
            "reddit": mock_reddit,
            "openai": mock_openai,
            "youtube": mock_youtube,
            "requests": mock_requests,
        }


class PerformanceTestHelper:
    """Helper class for performance testing."""

    @staticmethod
    def time_operation(operation, *args, **kwargs):
        """Time an operation and return duration and result."""
        import time

        start_time = time.time()
        result = operation(*args, **kwargs)
        end_time = time.time()

        duration = end_time - start_time
        return duration, result

    @staticmethod
    def assert_performance_threshold(
        operation, threshold_seconds: float, *args, **kwargs
    ):
        """Assert that an operation completes within a time threshold."""
        duration, result = PerformanceTestHelper.time_operation(
            operation, *args, **kwargs
        )

        if duration > threshold_seconds:
            raise AssertionError(
                f"Operation took {duration:.3f}s, which exceeds threshold of {threshold_seconds}s"
            )

        return result


class FileTestHelper:
    """Helper class for file system testing."""

    @staticmethod
    def create_test_directory_structure(base_path: Path):
        """Create a standard test directory structure."""
        directories = ["config", "data", "outputs", "logs"]

        for directory in directories:
            (base_path / directory).mkdir(parents=True, exist_ok=True)

        return base_path

    @staticmethod
    def cleanup_test_files(base_path: Path):
        """Clean up test files and directories."""
        import shutil

        if base_path.exists() and base_path.is_dir():
            shutil.rmtree(base_path)


# Pytest markers for categorizing tests
def mark_slow(test_func):
    """Mark a test as slow-running."""
    import pytest

    return pytest.mark.slow(test_func)


def mark_integration(test_func):
    """Mark a test as an integration test."""
    import pytest

    return pytest.mark.integration(test_func)


def mark_unit(test_func):
    """Mark a test as a unit test."""
    import pytest

    return pytest.mark.unit(test_func)


def mark_config(test_func):
    """Mark a test as config-related."""
    import pytest

    return pytest.mark.config(test_func)
