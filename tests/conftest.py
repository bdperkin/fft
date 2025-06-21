# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Brandon Perkins <bdperkin@gmail.com>

"""Pytest configuration and shared fixtures for FFT tests."""

import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content")
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def python_file():
    """Create a temporary Python file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
        f.write("#!/usr/bin/env python3\nimport os\nprint('hello world')")
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def executable_file():
    """Create a temporary executable file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("#!/bin/bash\necho 'hello'")
        f.flush()
        os.chmod(f.name, 0o755)
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def json_file():
    """Create a temporary JSON file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        f.write('{"name": "test", "version": "1.0.0"}')
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def html_file():
    """Create a temporary HTML file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html") as f:
        html_content = (
            "<!DOCTYPE html>\n<html><head><title>Test</title></head>"
            "<body><h1>Hello</h1></body></html>"
        )
        f.write(html_content)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def markdown_file():
    """Create a temporary Markdown file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md") as f:
        f.write(
            "# Test Document\n\nThis is a **test** markdown file.\n\n- Item 1\n- Item 2"
        )
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def symlink_file(temp_dir):
    """Create a symbolic link for testing."""
    target_file = os.path.join(temp_dir, "target.txt")
    link_file = os.path.join(temp_dir, "link.txt")

    Path(target_file).touch()
    os.symlink(target_file, link_file)

    yield link_file
