# Contributing to FFT

Thank you for your interest in contributing to FFT (File Type Tester)! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Making Changes](#making-changes)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

## Code of Conduct

This project follows a Code of Conduct to ensure a welcoming environment for all contributors. Please be respectful and considerate in all interactions.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Git
- libmagic library (for file type detection)

**System Dependencies:**

Ubuntu/Debian:
```bash
sudo apt-get install libmagic1
```

RHEL/CentOS/Fedora:
```bash
sudo dnf install file-libs
```

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/fft.git
   cd fft
   ```

## Development Environment

### Install Development Dependencies

```bash
# Install the package in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Verify Setup

```bash
# Test the application
./fft.py --help

# Run pre-commit checks
pre-commit run --all-files
```

## Making Changes

### Branching Strategy

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

2. Make your changes in logical, atomic commits
3. Write descriptive commit messages

### Commit Message Format

Use clear, descriptive commit messages:

```
Add support for detecting WebAssembly files

- Implement .wasm file extension detection
- Add magic number detection for WASM files
- Update tests to cover WebAssembly files
- Update documentation with new file type
```

## Code Standards

This project maintains high code quality standards using automated tools:

### Code Quality Tools

- **Black**: Code formatting (88-character line length)
- **Flake8**: Linting and style checking
- **isort**: Import sorting
- **MyPy**: Type checking
- **Pre-commit hooks**: Various checks (trailing whitespace, YAML/TOML validation, etc.)

### Running Code Quality Checks

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run individual tools
black fft.py
flake8 fft.py
isort fft.py
mypy fft.py
```

### Code Style Guidelines

- Follow PEP 8 with 88-character line length (Black default)
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and reasonably sized
- Use descriptive variable and function names

### Adding New File Types

When adding support for new file types:

1. **Filesystem tests**: Add file extensions to the `extension_map` in `filesystem_tests()`
2. **Magic tests**: The libmagic library handles this automatically for most files
3. **Language tests**: Add regex patterns to the `patterns` list in `language_tests()`

Example for adding TypeScript support:
```python
# In filesystem_tests extension_map
".ts": "TypeScript file",

# In language_tests patterns
(r"^interface\s+\w+|^class\s+\w+.*{|^import.*from.*['\"]", "TypeScript file"),
```

## Testing

### Manual Testing

Test your changes with various file types:

```bash
# Test basic functionality
./fft.py fft.py README.md pyproject.toml

# Test verbose mode
./fft.py -v fft.py README.md pyproject.toml

# Test edge cases
./fft.py /dev/null . /nonexistent/file
```

### Test Cases to Verify

- [ ] Executable files (scripts with shebangs)
- [ ] Various file extensions
- [ ] Directory detection
- [ ] Device files (`/dev/null`, `/dev/zero`)
- [ ] Symlinks
- [ ] Binary files
- [ ] Text files without extensions
- [ ] Files with multiple possible types
- [ ] Non-existent files (error handling)

## Submitting Changes

### Before Submitting

1. Ensure all pre-commit hooks pass:
   ```bash
   pre-commit run --all-files
   ```

2. Test your changes thoroughly
3. Update documentation if needed
4. Add entries to CHANGELOG.md if appropriate

### Pull Request Process

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request on GitHub with:
   - Clear title and description
   - Reference to related issues
   - Description of changes made
   - Testing performed

3. Ensure the PR passes all checks
4. Respond to review feedback promptly

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Manual testing performed
- [ ] All pre-commit hooks pass
- [ ] No regressions introduced

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated (if needed)
```

## Reporting Issues

### Bug Reports

When reporting bugs, include:

- FFT version (`./fft.py --help` shows version info)
- Python version
- Operating system
- File types that are incorrectly detected
- Expected vs. actual behavior
- Minimal reproduction steps

### Issue Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run `./fft.py [file]`
2. See error/incorrect detection

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.9.7]
- FFT version: [e.g., 1.3.0]

**Additional context**
Add any other context about the problem here.
```

## Feature Requests

Feature requests are welcome! When suggesting new features:

- Explain the use case and motivation
- Describe the proposed solution
- Consider backward compatibility
- Be open to discussion and alternatives

## Development Tips

### Debugging File Detection

Use verbose mode to understand which test detects files:
```bash
./fft.py -v mysterious_file
```

### Understanding the Detection Chain

FFT uses a three-tier detection system:
1. **Filesystem tests** (fastest): Extensions, permissions, file types
2. **Magic tests** (reliable): File signatures using libmagic
3. **Language tests** (content-based): Pattern matching in file content

### Adding Debug Output

For development, you can add temporary debug prints:
```python
print(f"DEBUG: Testing {filepath} with {test_name}")
```

Remember to remove debug output before submitting.

## Questions?

If you have questions about contributing:

- Check existing issues and discussions
- Create a new issue with the "question" label
- Be specific about what you're trying to accomplish

## Recognition

Contributors will be recognized in the project documentation. Thank you for helping make FFT better!

---

*This contributing guide is based on best practices from the open source community and is designed to make contributing to FFT as smooth as possible.*
