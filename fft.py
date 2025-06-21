#!/usr/bin/env python3
# Copyright (c) 2025 Brandon Perkins
# SPDX-License-Identifier: MIT
#
# This file is part of FFT (File Type Tester).
# See LICENSE file for full license details.

"""
FFT - File Type Tester
Determines the file type of files using filesystem, magic, and language tests.
"""

__version__ = "1.3.0"

import argparse
import mimetypes
import os
import re
import sys
from pathlib import Path

import magic


class FileTypeTester:
    def __init__(self, debug=False):
        self.debug = debug
        self.mime_detector = magic.Magic(magic.MAGIC_MIME_TYPE)
        self.description_detector = magic.Magic(magic.MAGIC_NONE)

    def debug_print(self, message):
        """Print debug message to stderr if debug mode is enabled"""
        if self.debug:
            print(f"DEBUG: {message}", file=sys.stderr)

    def filesystem_tests(self, filepath):
        """
        Filesystem-based tests: check extension, permissions, special files
        """
        self.debug_print(f"Running filesystem tests on '{filepath}'")
        path = Path(filepath)

        # Check if it's a directory
        if path.is_dir():
            self.debug_print(f"'{filepath}' is a directory")
            return "directory"

        # Check if it's a symbolic link
        if path.is_symlink():
            self.debug_print(f"'{filepath}' is a symbolic link")
            return "symbolic link"

        # Check if it's a block or character device
        if path.is_block_device():
            self.debug_print(f"'{filepath}' is a block device")
            return "block device"
        if path.is_char_device():
            self.debug_print(f"'{filepath}' is a character device")
            return "character device"

        # Check if it's a FIFO or socket
        if path.is_fifo():
            self.debug_print(f"'{filepath}' is a FIFO")
            return "FIFO (named pipe)"
        if path.is_socket():
            self.debug_print(f"'{filepath}' is a socket")
            return "socket"

        # Check executable permissions
        if os.access(filepath, os.X_OK) and path.is_file():
            self.debug_print(f"'{filepath}' has executable permissions")
            # Check if it starts with shebang
            try:
                with open(filepath, "rb") as f:
                    first_bytes = f.read(2)
                    if first_bytes == b"#!":
                        self.debug_print(
                            f"'{filepath}' has shebang, detected as executable script"
                        )
                        return "executable script"
            except (IOError, OSError) as e:
                self.debug_print(f"Failed to read first bytes of '{filepath}': {e}")
                pass
            self.debug_print(f"'{filepath}' is executable but no shebang detected")
            return "executable file"

        # Check common extensions
        extension = path.suffix.lower()
        self.debug_print(f"'{filepath}' has extension: '{extension}'")
        extension_map = {
            ".txt": "text file",
            ".py": "Python script",
            ".js": "JavaScript file",
            ".html": "HTML document",
            ".css": "CSS stylesheet",
            ".json": "JSON data",
            ".xml": "XML document",
            ".csv": "CSV data",
            ".md": "Markdown document",
            ".jpg": "JPEG image",
            ".jpeg": "JPEG image",
            ".png": "PNG image",
            ".gif": "GIF image",
            ".pdf": "PDF document",
            ".zip": "ZIP archive",
            ".tar": "TAR archive",
            ".gz": "GZIP compressed file",
            ".exe": "Windows executable",
            ".dll": "Windows DLL",
            ".so": "shared library",
            ".a": "static library",
            ".o": "object file",
            ".c": "C source file",
            ".cpp": "C++ source file",
            ".h": "C/C++ header file",
            ".java": "Java source file",
            ".class": "Java bytecode",
            ".rb": "Ruby script",
            ".php": "PHP script",
            ".sh": "shell script",
            ".bat": "batch file",
            ".ps1": "PowerShell script",
        }

        if extension in extension_map:
            result = extension_map[extension]
            self.debug_print(f"Extension '{extension}' mapped to: {result}")
            return result

        self.debug_print(f"Extension '{extension}' not found in mapping")
        return None

    def magic_tests(self, filepath):
        """
        Magic number tests using libmagic
        """
        self.debug_print(f"Running magic tests on '{filepath}'")
        try:
            # Get MIME type
            mime_type = self.mime_detector.from_file(filepath)
            self.debug_print(f"Magic MIME type for '{filepath}': {mime_type}")

            # Get file description
            description = self.description_detector.from_file(filepath)
            self.debug_print(f"Magic description for '{filepath}': {description}")

            # Return a more readable format
            if mime_type and description:
                result = f"{description} ({mime_type})"
                self.debug_print(f"Magic test result for '{filepath}': {result}")
                return result
            elif mime_type:
                result = f"file of type {mime_type}"
                self.debug_print(f"Magic test result for '{filepath}': {result}")
                return result
            elif description:
                self.debug_print(f"Magic test result for '{filepath}': {description}")
                return description

        except Exception as e:
            self.debug_print(f"Magic test failed for '{filepath}': {e}")
            # Fallback to Python's mimetypes module
            mime_type, _ = mimetypes.guess_type(filepath)
            if mime_type:
                result = f"file of type {mime_type}"
                self.debug_print(
                    f"Fallback mimetypes result for '{filepath}': {result}"
                )
                return result

        self.debug_print(f"Magic tests found no result for '{filepath}'")
        return None

    def language_tests(self, filepath):
        """
        Language detection tests based on file content analysis
        """
        self.debug_print(f"Running language tests on '{filepath}'")
        try:
            # Try to read the file as text
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(1024)  # Read first 1KB

            self.debug_print(f"Read {len(content)} characters from '{filepath}'")

            # Check for specific language patterns
            patterns = [
                (
                    r"#!/usr/bin/env python|#!/usr/bin/python|^import\s+\w+"
                    r"|^from\s+\w+\s+import",
                    "Python script",
                ),
                (r"#!/bin/bash|#!/bin/sh|^#\s*bash|^#\s*shell", "shell script"),
                (
                    r"^#!/usr/bin/env node|^const\s+\w+|^let\s+\w+|^var\s+\w+",
                    "JavaScript file",
                ),
                (r'^#include\s*<.*>|^#include\s*".*"|int\s+main\s*\(', "C/C++ source"),
                (
                    r"^package\s+\w+|^public\s+class\s+\w+|^import\s+java\.",
                    "Java source",
                ),
                (r"^<\?php|<\?=|\$\w+\s*=", "PHP script"),
                (r"^class\s+\w+|^def\s+\w+|^module\s+\w+", "Ruby script"),
                (r"^<!DOCTYPE html|^<html|^<head>|^<body>", "HTML document"),
                (r'^\s*{|\s*"[\w-]+"\s*:', "JSON data"),
                (r"^<\?xml|^<[a-zA-Z][^>]*>", "XML document"),
                (r"^\s*[\w-]+\s*:\s*[\w-]+|^\s*\.|^\s*#[a-zA-Z]", "CSS stylesheet"),
                (r"^#+\s+\w+|^\*\s+\w+|^\d+\.\s+\w+", "Markdown document"),
            ]

            for pattern, file_type in patterns:
                if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                    self.debug_print(
                        f"Pattern '{pattern}' matched for '{filepath}', detected as: {file_type}"
                    )
                    return file_type

            # Check if it's mostly text
            printable_chars = sum(1 for c in content if c.isprintable() or c.isspace())
            if len(content) > 0:
                printable_ratio = printable_chars / len(content)
                self.debug_print(
                    f"Printable character ratio for '{filepath}': {printable_ratio:.2f}"
                )
                if printable_ratio > 0.7:
                    self.debug_print(
                        f"'{filepath}' detected as text file based on printable character ratio"
                    )
                    return "text file"

        except (UnicodeDecodeError, IOError, OSError) as e:
            self.debug_print(f"Language test failed for '{filepath}': {e}")
            pass

        self.debug_print(f"Language tests found no result for '{filepath}'")
        return None

    def detect_file_type(self, filepath, verbose=False):
        """
        Main detection method that runs tests in order
        """
        self.debug_print(f"Starting file type detection for '{filepath}'")

        if not os.path.exists(filepath):
            error_msg = f"ERROR: File '{filepath}' does not exist"
            self.debug_print(error_msg)
            return error_msg, None

        # Run tests in order
        tests = [
            ("Filesystem", self.filesystem_tests),
            ("Magic", self.magic_tests),
            ("Language", self.language_tests),
        ]

        for test_name, test_func in tests:
            self.debug_print(f"Trying {test_name} test for '{filepath}'")
            try:
                result = test_func(filepath)
                if result:
                    self.debug_print(
                        f"{test_name} test succeeded for '{filepath}': {result}"
                    )
                    if verbose:
                        return result, test_name
                    else:
                        return result, None
                else:
                    self.debug_print(
                        f"{test_name} test returned no result for '{filepath}'"
                    )
            except Exception as e:
                self.debug_print(f"{test_name} test failed for '{filepath}': {e}")
                # Continue to next test if current one fails
                continue

        self.debug_print(
            f"All tests completed for '{filepath}', no definitive type found"
        )
        if verbose:
            return "unknown file type", "None"
        else:
            return "unknown file type", None


def main():
    parser = argparse.ArgumentParser(
        description=(
            "FFT - File Type Tester: Determine file types using filesystem, "
            "magic, and language tests"
        )
    )
    parser.add_argument("files", nargs="+", help="Files or directories to analyze")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show which test category detected the file type",
    )
    parser.add_argument(
        "-b",
        "--brief",
        action="store_true",
        help="Do not prepend filenames to output lines (brief mode)",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively process directories (default when directory is given)",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Print internal debugging information to stderr",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show version information",
    )

    args = parser.parse_args()

    # Initialize the tester
    tester = FileTypeTester(debug=args.debug)

    def process_file(filepath):
        """Process a single file and output the result"""
        file_type, test_category = tester.detect_file_type(
            filepath, verbose=args.verbose
        )

        if args.brief:
            # Brief mode: only output the file type
            print(file_type)
        elif args.verbose and test_category:
            # Verbose mode: include test category
            print(f"{filepath}: {file_type} [{test_category} test]")
        else:
            # Default mode: filename and file type
            print(f"{filepath}: {file_type}")

    def get_files_from_directory(directory_path):
        """Recursively get all files from a directory"""
        if args.debug:
            print(
                f"DEBUG: Scanning directory '{directory_path}' for files",
                file=sys.stderr,
            )
        files = []
        try:
            for root, dirs, filenames in os.walk(directory_path):
                if args.debug:
                    print(
                        f"DEBUG: Found {len(filenames)} files in '{root}'",
                        file=sys.stderr,
                    )
                for filename in filenames:
                    full_path = os.path.join(root, filename)
                    files.append(full_path)
                    if args.debug:
                        print(
                            f"DEBUG: Added file '{full_path}' to processing list",
                            file=sys.stderr,
                        )
        except (OSError, PermissionError) as e:
            error_msg = f"ERROR: Cannot access directory '{directory_path}': {e}"
            print(error_msg)
            if args.debug:
                print(f"DEBUG: {error_msg}", file=sys.stderr)
        return files

    # Process each file or directory
    if args.debug:
        print(
            f"DEBUG: Processing {len(args.files)} argument(s): {args.files}",
            file=sys.stderr,
        )

    for filepath in args.files:
        path = Path(filepath)

        if path.is_dir():
            if args.debug:
                print(
                    f"DEBUG: '{filepath}' is a directory, processing recursively",
                    file=sys.stderr,
                )
            # Process directory recursively
            files_in_dir = get_files_from_directory(filepath)
            if files_in_dir:
                if args.debug:
                    print(
                        f"DEBUG: Found {len(files_in_dir)} files in directory '{filepath}', sorting...",
                        file=sys.stderr,
                    )
                for file_in_dir in sorted(files_in_dir):
                    process_file(file_in_dir)
            else:
                if args.debug:
                    print(
                        f"DEBUG: Directory '{filepath}' is empty or inaccessible",
                        file=sys.stderr,
                    )
                print(f"{filepath}: directory (empty or inaccessible)")
        else:
            if args.debug:
                print(
                    f"DEBUG: '{filepath}' is a file, processing directly",
                    file=sys.stderr,
                )
            # Process single file
            process_file(filepath)


if __name__ == "__main__":
    main()
