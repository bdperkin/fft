# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2024-12-19

### Added
- Pre-commit hooks for code quality assurance
- Development dependencies in `pyproject.toml` under `[dev]` section
- Comprehensive code quality tools:
  - Black for code formatting
  - Flake8 for linting and style checking
  - isort for import sorting
  - MyPy for type checking
  - Standard pre-commit hooks (trailing whitespace, end-of-file fixes, etc.)
- Development setup instructions in README.md

### Changed
- Code formatting applied throughout the project using Black
- Long lines broken to comply with 88-character limit
- Import statements organized with isort

### Fixed
- Removed unused `sys` import
- Removed unused exception variables
- Fixed flake8 linting issues
- Trailing whitespace and end-of-file issues

## [1.2.0] - 2024-12-19

### Changed
- **BREAKING**: Output format now always includes filenames
- Verbose mode (`-v`) now shows which test category detected the file type
- Enhanced user experience when analyzing multiple files

### Added
- Test category indicators in verbose mode (e.g., `[Filesystem test]`, `[Magic test]`, `[Language test]`)

### Updated
- README.md examples to reflect new output format
- Help text for verbose option to clarify new functionality

## [1.1.0] - 2024-12-19

### Changed
- **BREAKING**: Migrated from `setup.py` and `requirements.txt` to modern `pyproject.toml`
- Adopted PEP 621 standard for project metadata
- Updated installation instructions in README.md

### Added
- Modern build system using setuptools with `pyproject.toml`
- Project URLs section in configuration
- Note about PEP 621 compliance in README.md

### Removed
- `setup.py` file (replaced by `pyproject.toml`)
- `requirements.txt` file (dependencies now in `pyproject.toml`)

## [1.0.0] - 2024-12-19

### Added
- Initial implementation of FFT (File Type Tester)
- Three-tier file type detection system:
  1. **Filesystem tests**: Extensions, permissions, special files
  2. **Magic tests**: MIME type detection using libmagic
  3. **Language tests**: Content-based programming language detection
- Command-line interface with file arguments
- Verbose mode option (`-v`)
- Support for detecting:
  - Directories, symbolic links, device files
  - Executable files with shebang detection
  - 25+ file extensions
  - Programming languages (Python, JavaScript, C/C++, Java, etc.)
  - Markup languages (HTML, XML, JSON, CSS, Markdown)
  - Binary files and archives
- Comprehensive documentation in README.md
- MIT License
- Python 3.6+ compatibility
- Dependency on python-magic for file signature detection

### Technical Features
- Fallback detection chain (filesystem → magic → language → unknown)
- Error handling for missing files and permission issues
- Content analysis for text file detection
- Pattern matching for programming language identification
- Cross-platform compatibility

---

## Version History Summary

- **v1.3.0**: Added pre-commit hooks and code quality tools
- **v1.2.0**: Enhanced output format with mandatory filename prefixes
- **v1.1.0**: Modernized to pyproject.toml build system
- **v1.0.0**: Initial release with core file type detection functionality

[Unreleased]: https://github.com/user/fft/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/user/fft/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/user/fft/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/fft/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/user/fft/releases/tag/v1.0.0
