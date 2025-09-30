# Test Suite for TheThinkle.ai

This directory contains the comprehensive test suite for the TheThinkle.ai newsletter generation system.

## Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   └── test_config_parser.py   # Config parser tests
├── integration/             # Integration tests for component interactions
│   └── test_pipeline.py        # Pipeline integration tests
├── fixtures/                # Test data and fixtures
│   ├── sample_configs.py       # Configuration test data
│   └── sample_data.py          # Mock API responses and data
├── test_utils.py           # Test utilities and helpers
└── README.md               # This file
```

## Running Tests

### Quick Start
```bash
# Run all tests
make test

# Run specific test categories
make test-unit          # Unit tests only
make test-integration   # Integration tests only
make test-config        # Config-related tests only

# Run with coverage
make test-coverage
```

### Using pytest directly
```bash
# Run all tests
pytest

# Run specific test files
pytest tests/unit/test_config_parser.py
pytest tests/integration/test_pipeline.py

# Run tests with specific markers
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m config        # Config tests only
pytest -m "not slow"    # Skip slow tests

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html
```

## Test Categories

### Unit Tests (`tests/unit/`)
Test individual components in isolation:
- **Config Parser Tests**: Comprehensive validation of Pydantic models, YAML parsing, error handling
- **Agent Tests**: (Future) Individual agent functionality
- **Tool Tests**: (Future) Data source tool functionality

### Integration Tests (`tests/integration/`)
Test component interactions:
- **Pipeline Tests**: End-to-end workflow testing
- **Component Integration**: How different parts work together
- **Error Handling**: System resilience testing

### Test Fixtures (`tests/fixtures/`)
Reusable test data:
- **Sample Configurations**: Valid and invalid config scenarios
- **Mock Data**: Sample API responses, articles, social media posts
- **Test Utilities**: Helper functions and classes

## Test Markers

Tests are categorized with pytest markers:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests  
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.api` - Tests requiring external API access
- `@pytest.mark.config` - Configuration-related tests

## Writing Tests

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `TestComponentName`
- Test methods: `test_specific_behavior`

### Example Test Structure
```python
class TestConfigParser:
    """Test the ConfigParser class."""
    
    def test_load_valid_config(self, temp_config_file):
        """Test loading a valid configuration file."""
        parser = ConfigParser(temp_config_file)
        config = parser.load_config()
        
        assert isinstance(config, ThinkleConfig)
        assert len(config.interests) > 0
    
    def test_validation_error(self):
        """Test proper handling of validation errors."""
        with pytest.raises(ValidationError):
            ThinkleConfig(interests=[])
```

### Using Fixtures
```python
def test_with_sample_config(self, sample_config):
    """Test using the sample_config fixture."""
    assert sample_config.newsletter.tone in ["professional", "witty", "casual", "academic"]

def test_with_temp_file(self, temp_config_file):
    """Test using a temporary config file."""
    parser = ConfigParser(temp_config_file)
    config = parser.load_config()
    assert config is not None
```

### Mocking External Dependencies
```python
def test_with_mocked_apis(self, mock_openai_client, mock_reddit_client):
    """Test with mocked external APIs."""
    # Test logic here - external APIs are automatically mocked
    pass
```

## Coverage Goals

- **Unit Tests**: >95% coverage for individual components
- **Integration Tests**: Cover all major workflows
- **Error Handling**: Test all error scenarios
- **Configuration**: Test all validation rules

## Continuous Integration

The test suite is designed to run in CI/CD environments:

```bash
# CI-friendly test command
make ci-test

# Generates XML reports for CI systems
pytest --cov=. --cov-report=xml --junitxml=test-results.xml
```

## Performance Testing

Some tests are marked as `@pytest.mark.slow` for performance testing:

```bash
# Run only performance tests
pytest -m slow

# Skip slow tests for faster feedback
pytest -m "not slow"
```

## Debugging Tests

### Running Single Tests
```bash
# Run specific test
pytest tests/unit/test_config_parser.py::TestThinkleConfig::test_valid_config -v

# Run with debugging output
pytest tests/unit/test_config_parser.py::TestThinkleConfig::test_valid_config -v -s
```

### Test Output
```bash
# Show print statements
pytest -s

# Show full diff on failures
pytest --tb=long

# Show only short traceback
pytest --tb=short
```

## Adding New Tests

1. **Choose the right category**: Unit vs Integration
2. **Use appropriate fixtures**: Leverage existing test data
3. **Add proper markers**: `@pytest.mark.unit`, etc.
4. **Follow naming conventions**: Clear, descriptive names
5. **Test both success and failure cases**
6. **Mock external dependencies** appropriately

## Test Configuration

Test configuration is managed through:
- `pytest.ini` - Pytest settings and markers
- `conftest.py` - Global fixtures and configuration
- `Makefile` - Convenient test commands

## Future Test Areas

As the system grows, tests will be added for:
- **Agent Components**: Planner, Scout, Investigator, Evaluator, Writer
- **Data Tools**: Reddit, YouTube, ArXiv, News scrapers
- **Content Processing**: Summarization, scoring, filtering
- **Output Generation**: Markdown, PDF, HTML formatting
- **Pipeline Orchestration**: Full end-to-end workflows
