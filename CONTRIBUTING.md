# Contributing to Flynn

First off, thank you for considering contributing to Flynn! 🎉

Flynn is a community-driven project, and we welcome contributions from everyone. This document provides guidelines and information about contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

## 📜 Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to support@synetalsolutions.com.

## 🤔 How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check if the issue already exists. When creating a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs. actual behavior
- **Environment details** (OS, Python version, Docker version)
- **Logs or error messages** if applicable

### Suggesting Features

Feature suggestions are welcome! Please:

- Check if the feature has already been suggested
- Provide a clear description of the feature
- Explain why this feature would be useful
- Include examples of how it would work

### Contributing Code

1. Look for issues labeled `good first issue` or `help wanted`
2. Comment on the issue to let others know you're working on it
3. Fork the repository and create your branch
4. Write your code and tests
5. Submit a pull request

## 🛠️ Development Setup

### Prerequisites

- Python 3.12+
- Docker Desktop or Docker Engine
- [uv](https://github.com/astral-sh/uv) package manager

### Setting Up Your Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Flynn.git
cd Flynn

# Install dependencies (including dev dependencies)
uv sync --all-extras

# Verify installation
uv run flynn --help
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=flynn

# Run specific test file
uv run pytest tests/test_handlers.py
```

### Linting and Formatting

```bash
# Check code style
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Type checking
uv run mypy src/flynn
```

## 🔄 Pull Request Process

1. **Create a branch** from `main` with a descriptive name:
   - `feature/add-volume-support`
   - `fix/container-logs-error`
   - `docs/update-readme`

2. **Make your changes** following our style guidelines

3. **Write tests** for any new functionality

4. **Update documentation** if needed

5. **Run all checks** before submitting:
   ```bash
   uv run ruff check .
   uv run pytest
   ```

6. **Submit your PR** with:
   - Clear title describing the change
   - Description of what changed and why
   - Reference to any related issues

7. **Respond to feedback** from reviewers

## 📝 Style Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/)
- Use [ruff](https://github.com/astral-sh/ruff) for linting
- Maximum line length: 100 characters
- Use type hints for all function parameters and return values

### Commits

- Use clear, descriptive commit messages
- Start with a verb in present tense: "Add", "Fix", "Update"
- Reference issues when applicable: "Fix #123: Handle timeout error"

### Documentation

- Use docstrings for all public functions and classes
- Update README.md for user-facing changes
- Include examples in docstrings when helpful

## 🌍 Community

- **GitHub Discussions**: Ask questions and share ideas
- **Issues**: Report bugs and suggest features
- **Email**: support@synetalsolutions.com

---

Thank you for contributing to Flynn! 🚀
