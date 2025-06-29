# Makefile for FFT (File Type Tester)
# Copyright (c) 2025 Brandon Perkins <bdperkin@gmail.com>
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
all: help

docs-all: docs pdf

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
	$(PYTHON) -m pip install -e ".[dev]"
	pre-commit install
	@echo "Note: cspell is a Node.js package and must be installed separately:"
	@echo "  npm install -g cspell"
	@echo "  or use your system package manager"

test:
	pytest

lint:
	pre-commit run --all-files

format:
	black $(PYTHON_SOURCE)
	isort $(PYTHON_SOURCE)

check:
	flake8 --max-line-length=88 --extend-ignore=E203 $(PYTHON_SOURCE)
	mypy $(PYTHON_SOURCE)

coverage:
	pytest --cov=fft --cov-report=html --cov-report=term-missing

# Build and package
build:
	@echo "Building distribution packages..."
	$(PYTHON) -m build
	@echo "Build complete. Files created in dist/:"
	@ls -la dist/

install:
	$(PYTHON) -m pip install -e .

# RPM packaging
srpm: clean-all
	@echo "Building source RPM..."
	@VERSION=$(shell grep '^__version__' $(PYTHON_SOURCE) | cut -d'"' -f2); \
	echo "Creating source tarball for version $$VERSION..."; \
	git archive --format=tar.gz --prefix=fft-$$VERSION/ HEAD > fft-$$VERSION.tar.gz; \
	echo "Building source RPM..."; \
	rpmbuild -ts fft-$$VERSION.tar.gz \
		--define "_sourcedir $(PWD)" \
		--define "_specdir $(PWD)" \
		--define "_builddir $(PWD)/build" \
		--define "_srcrpmdir $(PWD)" \
		--define "_rpmdir $(PWD)"; \
	echo "Source RPM build complete. Files created:"; \
	ls -la fft-$$VERSION.tar.gz python3-fft-$$VERSION-1.*.src.rpm

rpm: srpm
	@echo "Building binary RPM..."
	@VERSION=$(shell grep '^__version__' $(PYTHON_SOURCE) | cut -d'"' -f2); \
	rpmbuild --rebuild python3-fft-$$VERSION-1.*.src.rpm \
		--define "_rpmdir $(PWD)" \
		--define "_builddir $(PWD)/build"; \
	echo "Binary RPM build complete. Files created:"; \
	ls -la python3-fft-$$VERSION-1.*.src.rpm noarch/python3-fft-$$VERSION-1.*.noarch.rpm 2>/dev/null || true

rpm-install: rpm
	@echo "Installing RPM package..."
	sudo rpm -Uvh noarch/python3-fft-$(shell grep '^__version__' $(PYTHON_SOURCE) | cut -d'"' -f2)-1.*.noarch.rpm

rpm-test: rpm
	@echo "Testing RPM packages..."
	rpm -qpl python3-fft-$(shell grep '^__version__' $(PYTHON_SOURCE) | cut -d'"' -f2)-1.*.src.rpm
	rpm -qpl noarch/python3-fft-$(shell grep '^__version__' $(PYTHON_SOURCE) | cut -d'"' -f2)-1.*.noarch.rpm

clean:
	rm -f $(INFO_FILE)
	rm -f $(HTML_DOC)
	rm -f $(PDF_DOC)
	rm -f *.aux *.cp *.cps *.fn *.ky *.log *.pg *.toc *.tp *.vr
	rm -f *.html *.pdf
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
	rm -f *.tar.gz
	rm -f *.src.rpm
	rm -rf noarch/

# Version update
update-version:
	@echo "Current version in fft.py:"
	@grep "^__version__" $(PYTHON_SOURCE)
	@echo "Current version in fft.texi:"
	@grep "VERSION" $(TEXI_SOURCE)

# Help target
help:
	@echo "Available targets:"
	@echo "  all         - Show this help message (default)"
	@echo "  docs-all    - Build all documentation (info, HTML, PDF)"
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
	@echo "  srpm        - Build source RPM package"
	@echo "  rpm         - Build binary RPM package"
	@echo "  rpm-install - Build and install RPM package"
	@echo "  rpm-test    - Build and test RPM package contents"
	@echo "  clean       - Remove generated files"
	@echo "  clean-all   - Remove all generated and build files"
	@echo "  update-version - Show current version information"
	@echo "  help        - Show this help message"

.PHONY: all docs-all docs info html pdf test-man test-info install-dev test lint format check coverage build install srpm rpm rpm-install rpm-test clean clean-all update-version help
