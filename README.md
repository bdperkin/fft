# FFT - File Type Tester

A Python 3 project that determines the file type of files using three different test categories performed in sequence:

1. **Filesystem Tests** - Check file extensions, permissions, and filesystem attributes
2. **Magic Tests** - Use libmagic to detect file types based on file signatures
3. **Language Tests** - Analyze file content to detect programming languages and text formats

The first test that successfully identifies the file type will be reported.

## Installation

### Requirements

- Python 3.6 or higher
- libmagic library (for magic number detection)

This project uses the modern `pyproject.toml` build system (PEP 621).

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

For contributing guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

On Ubuntu/Debian:
```bash
sudo apt-get install libmagic1
```

On RHEL/CentOS/Fedora:
```bash
sudo dnf install file-libs  # or: sudo yum install file-libs
```

### Install Dependencies

Install as a package (recommended):
```bash
pip install -e .
```

Or install dependencies manually:
```bash
pip install python-magic>=0.4.24
```

### Development Setup

For development with code quality tools:
```bash
pip install -e ".[dev]"
pre-commit install
```

Run pre-commit on all files:
```bash
pre-commit run --all-files
```

Run tests:
```bash
pytest
```

Build documentation:
```bash
make docs  # Build info and HTML documentation
make help  # Show all available Makefile targets
```

## Usage

### Direct Script Execution

```bash
./fft.py file1.txt file2.py file3.jpg
```

### With verbose output (shows which test detected the file type)

```bash
./fft.py -v file1.txt file2.py file3.jpg
```

### After package installation

```bash
fft file1.txt file2.py file3.jpg
```

### View documentation

```bash
# Manual page
man fft

# Info documentation (hierarchical, cross-referenced)
info fft

# HTML documentation (if generated)
# See fft.html or run: make html
```

(Note: Documentation is included in the package and available after installation)

## Test Categories

### 1. Filesystem Tests
- Directory detection
- Symbolic links
- Device files (block/character)
- FIFO pipes and sockets
- Executable files (with shebang detection)
- File extensions (comprehensive mapping)

### 2. Magic Tests
- MIME type detection using libmagic
- File signature analysis
- Fallback to Python's mimetypes module

### 3. Language Tests
- Content-based programming language detection
- Pattern matching for:
  - Python, JavaScript, C/C++, Java
  - Shell scripts, PHP, Ruby
  - HTML, XML, JSON, CSS
  - Markdown documents
- Text file detection based on printable character ratio

## Development

This project uses pre-commit hooks to maintain code quality:

- **Black**: Code formatting
- **Flake8**: Linting and style checking
- **isort**: Import sorting
- **MyPy**: Type checking
- **Standard hooks**: Trailing whitespace, YAML/TOML validation, etc.

## Examples

```bash
$ ./fft.py fft.py pyproject.toml README.md
fft.py: executable script
pyproject.toml: JSON data
README.md: Markdown document

$ ./fft.py -v fft.py pyproject.toml README.md
fft.py: executable script [Filesystem test]
pyproject.toml: JSON data [Language test]
README.md: Markdown document [Filesystem test]
```
Find files based on filesystem, magic, and language.
