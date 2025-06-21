# Makefile for FFT (File Type Tester)
# Copyright (c) 2024 Brandon Perkins <bdperkin@gmail.com>
# SPDX-License-Identifier: MIT

# Variables
PYTHON = python3
PIP = pip
MAKEINFO = makeinfo
GROFF = groff

# Source files
TEXI_SOURCE = fft.texi
MAN_SOURCE = fft.1
PYTHON_SOURCE = fft.py

# Generated files
INFO_FILE = fft.info
HTML_DOC = fft.html
PDF_DOC = fft.pdf

# Default target
all: docs

# Documentation targets
docs: info html

info: $(INFO_FILE)

$(INFO_FILE): $(TEXI_SOURCE)
	$(MAKEINFO) $(TEXI_SOURCE)

html: $(HTML_DOC)

$(HTML_DOC): $(TEXI_SOURCE)
	$(MAKEINFO) --html --no-split $(TEXI_SOURCE)

pdf: $(PDF_DOC)

$(PDF_DOC): $(TEXI_SOURCE)
	texi2pdf $(TEXI_SOURCE)

# Test the man page
test-man:
	$(GROFF) -man -Tascii $(MAN_SOURCE) | head -20

# Test the info file
test-info:
	info --file=./$(INFO_FILE) --node=Top --output=- | head -20

# Development targets
install-dev:
	$(PIP) install -e ".[dev]"
	pre-commit install

test:
	pytest

lint:
	pre-commit run --all-files

format:
	black $(PYTHON_SOURCE)
	isort $(PYTHON_SOURCE)

check:
	flake8 $(PYTHON_SOURCE)
	mypy $(PYTHON_SOURCE)

coverage:
	pytest --cov=fft --cov-report=html --cov-report=term-missing

# Build and package
build:
	$(PYTHON) -m build

install:
	$(PIP) install -e .

clean:
	rm -f $(INFO_FILE)
	rm -f $(HTML_DOC)
	rm -f $(PDF_DOC)
	rm -f *.aux *.cp *.fn *.ky *.log *.pg *.toc *.tp *.vr
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	rm -rf tests/__pycache__/
	rm -f .coverage
	rm -f coverage.xml

clean-all: clean
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf build/

# Version update
update-version:
	@echo "Current version in fft.py:"
	@grep "__version__" $(PYTHON_SOURCE)
	@echo "Current version in fft.texi:"
	@grep "VERSION" $(TEXI_SOURCE)

# Help target
help:
	@echo "Available targets:"
	@echo "  all         - Build all documentation (default)"
	@echo "  docs        - Build info and HTML documentation"
	@echo "  info        - Build info documentation"
	@echo "  html        - Build HTML documentation"
	@echo "  pdf         - Build PDF documentation"
	@echo "  test-man    - Test man page rendering"
	@echo "  test-info   - Test info file"
	@echo "  install-dev - Install development dependencies"
	@echo "  test        - Run pytest test suite"
	@echo "  lint        - Run all pre-commit hooks"
	@echo "  format      - Format code with black and isort"
	@echo "  check       - Run linting and type checking"
	@echo "  coverage    - Run tests with coverage report"
	@echo "  build       - Build distribution packages"
	@echo "  install     - Install package in development mode"
	@echo "  clean       - Remove generated files"
	@echo "  clean-all   - Remove all generated and build files"
	@echo "  update-version - Show current version information"
	@echo "  help        - Show this help message"

.PHONY: all docs info html pdf test-man test-info install-dev test lint format check coverage build install clean clean-all update-version help
