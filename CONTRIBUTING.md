# Contributing to TheThinkle.ai

Thank you for your interest in contributing to TheThinkle.ai! This document provides guidelines and information for contributors.

## 🚀 Getting Started

1. **Fork the repository** and clone your fork locally
2. **Set up your development environment** following the README.md instructions
3. **Create a feature branch** from `main`
4. **Make your changes** following our coding standards
5. **Test your changes** thoroughly
6. **Submit a pull request**

## 📝 Coding Standards

### Code Style

- **Formatting**: We use [Black](https://github.com/psf/black) with default settings (88 characters)
- **Linting**: We use [Flake8](https://flake8.pycqa.org/) for code quality checks
- **Type Hints**: All functions should include type hints
- **Docstrings**: Use Google-style docstrings for all modules, classes, and public functions

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
    pass
```

### Naming Conventions

- **Functions/Variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`

### Before Committing

```bash
# Format your code
make format

# Run linting
make lint

# Run tests
make test

# Or run all at once
make dev
```

## 🧪 Testing

- **Unit tests** are required for all new functionality
- Place tests in `tests/unit/` mirroring the module structure
- Integration tests go in `tests/integration/`
- Use fixtures from `tests/fixtures/` for test data
- Aim for deterministic tests that don't require external API calls

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_config_parser.py

# Run with coverage
pytest --cov=. --cov-report=html
```

## 📋 Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(scout): add YouTube transcript fetching
fix(config): handle missing interests gracefully
docs(readme): update installation instructions
test(planner): add test for empty interests list
```

## 🔧 Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes**
   - Write code following our standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Test locally**
   ```bash
   make dev  # Format, lint, and test
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add awesome feature"
   ```

5. **Push and create PR**
   ```bash
   git push origin feat/your-feature-name
   ```

## 🎯 Pull Request Process

1. **Update documentation** if you've changed APIs or added features
2. **Ensure all tests pass** and add new tests if needed
3. **Fill out the PR template** with:
   - Description of changes
   - Related issue numbers (if applicable)
   - Screenshots/logs (if relevant)
4. **Wait for review** - maintainers will review your PR
5. **Address feedback** if requested
6. **Celebrate** when your PR is merged! 🎉

## 🐛 Reporting Bugs

When reporting bugs, please include:

- **Clear description** of the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Relevant logs** or error messages
- **Configuration** (sanitized `interests.yaml`, etc.)

## 💡 Suggesting Features

We welcome feature suggestions! Please:

- **Check existing issues** to avoid duplicates
- **Describe the problem** your feature would solve
- **Propose a solution** with implementation ideas
- **Consider alternatives** you've thought about

## 🤝 Code of Conduct

- **Be respectful** and constructive
- **Welcome newcomers** and help them learn
- **Focus on the code**, not the person
- **Assume good intentions**
- **Give credit** where credit is due

## 📞 Questions?

- **Open an issue** for bugs or feature requests
- **Start a discussion** for questions or ideas
- **Check the README** for common setup issues

## 🙏 Thank You!

Every contribution, no matter how small, helps make TheThinkle.ai better. We appreciate your time and effort!

---

**Happy coding!** 🧠✨
