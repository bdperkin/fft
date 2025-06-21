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

On Ubuntu/Debian:
```bash
sudo apt-get install libmagic1
```

On RHEL/CentOS/Fedora:
```bash
sudo dnf install file-libs  # or: sudo yum install file-libs
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install as a package:
```bash
pip install -e .
```

## Usage

### Direct Script Execution

```bash
./fft.py file1.txt file2.py file3.jpg
```

### With verbose output

```bash
./fft.py -v file1.txt file2.py file3.jpg
```

### After package installation

```bash
fft file1.txt file2.py file3.jpg
```

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

## Examples

```bash
$ ./fft.py fft.py setup.py README.md
Python script
Python script
Markdown document

$ ./fft.py -v fft.py setup.py README.md
fft.py: Python script
setup.py: Python script
README.md: Markdown document
```
Find files based on filesystem, magic, and language.
