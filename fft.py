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
    def __init__(self, debug=False, no_dereference=None, mime=False):
        self.debug = debug
        self.mime = mime

        # Handle no_dereference default based on POSIXLY_CORRECT environment variable
        if no_dereference is None:
            # Default is to NOT follow symlinks if POSIXLY_CORRECT is not defined
            self.no_dereference = os.environ.get("POSIXLY_CORRECT") is None
        else:
            self.no_dereference = no_dereference

        self.mime_detector = magic.Magic(magic.MAGIC_MIME_TYPE)
        self.description_detector = magic.Magic(magic.MAGIC_NONE)

        # Extension to file type mapping
        self.extension_map = {
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

        # MIME type mapping for filesystem tests
        self.extension_mime_map = {
            ".txt": "text/plain",
            ".py": "text/x-python",
            ".js": "text/javascript",
            ".html": "text/html",
            ".css": "text/css",
            ".json": "application/json",
            ".xml": "application/xml",
            ".csv": "text/csv",
            ".md": "text/markdown",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".pdf": "application/pdf",
            ".zip": "application/zip",
            ".tar": "application/x-tar",
            ".gz": "application/gzip",
            ".exe": "application/x-msdownload",
            ".dll": "application/x-msdownload",
            ".so": "application/x-sharedlib",
            ".a": "application/x-archive",
            ".o": "application/x-object",
            ".c": "text/x-c",
            ".cpp": "text/x-c++",
            ".h": "text/x-c",
            ".java": "text/x-java-source",
            ".class": "application/java-vm",
            ".rb": "text/x-ruby",
            ".php": "text/x-php",
            ".sh": "text/x-shellscript",
            ".bat": "text/x-msdos-batch",
            ".ps1": "text/x-powershell",
        }

        # File type to MIME type mapping for special filesystem types
        self.filesystem_mime_map = {
            "directory": "inode/directory",
            "symbolic link": "inode/symlink",
            "block device": "inode/blockdevice",
            "character device": "inode/chardevice",
            "FIFO (named pipe)": "inode/fifo",
            "socket": "inode/socket",
            "executable file": "application/x-executable",
            "executable script": "text/x-shellscript",
        }

        # Build reverse mapping for extension lookup
        self.type_to_extensions = {}
        for ext, file_type in self.extension_map.items():
            if file_type not in self.type_to_extensions:
                self.type_to_extensions[file_type] = []
            self.type_to_extensions[file_type].append(ext)

    def debug_print(self, message):
        """Print debug message to stderr if debug mode is enabled"""
        if self.debug:
            print(f"DEBUG: {message}", file=sys.stderr)

    def get_extensions_for_type(self, file_type):
        """Get a slash-separated list of extensions for a given file type"""
        if file_type in self.type_to_extensions:
            # Sort extensions and remove the leading dot for display
            extensions = sorted(self.type_to_extensions[file_type])
            return "/".join(ext[1:] for ext in extensions)  # Remove leading dot
        return ""

    def filesystem_tests(self, filepath):
        """
        Filesystem-based tests: check extension, permissions, special files
        """
        self.debug_print(f"Running filesystem tests on '{filepath}'")
        path = Path(filepath)

        # Check if it's a symbolic link first
        if path.is_symlink():
            self.debug_print(f"'{filepath}' is a symbolic link")
            if self.no_dereference:
                # Don't follow symlinks - return "symbolic link" or MIME
                self.debug_print(
                    f"Not dereferencing symlink '{filepath}' "
                    f"(no_dereference={self.no_dereference})"
                )
                if self.mime:
                    return self.filesystem_mime_map["symbolic link"]
                else:
                    return "symbolic link"
            else:
                # Follow symlinks - continue with analysis of the target
                self.debug_print(
                    f"Dereferencing symlink '{filepath}' "
                    f"(no_dereference={self.no_dereference})"
                )
                # Continue with normal analysis - the path methods will follow the link

        # Check if it's a directory
        if path.is_dir():
            self.debug_print(f"'{filepath}' is a directory")
            if self.mime:
                return self.filesystem_mime_map["directory"]
            else:
                return "directory"

        # Check if it's a block or character device
        if path.is_block_device():
            self.debug_print(f"'{filepath}' is a block device")
            if self.mime:
                return self.filesystem_mime_map["block device"]
            else:
                return "block device"
        if path.is_char_device():
            self.debug_print(f"'{filepath}' is a character device")
            if self.mime:
                return self.filesystem_mime_map["character device"]
            else:
                return "character device"

        # Check if it's a FIFO or socket
        if path.is_fifo():
            self.debug_print(f"'{filepath}' is a FIFO")
            if self.mime:
                return self.filesystem_mime_map["FIFO (named pipe)"]
            else:
                return "FIFO (named pipe)"
        if path.is_socket():
            self.debug_print(f"'{filepath}' is a socket")
            if self.mime:
                return self.filesystem_mime_map["socket"]
            else:
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
                        if self.mime:
                            return self.filesystem_mime_map["executable script"]
                        else:
                            return "executable script"
            except (IOError, OSError) as e:
                self.debug_print(f"Failed to read first bytes of '{filepath}': {e}")
                pass
            self.debug_print(f"'{filepath}' is executable but no shebang detected")
            if self.mime:
                return self.filesystem_mime_map["executable file"]
            else:
                return "executable file"

        # Check common extensions
        extension = path.suffix.lower()
        self.debug_print(f"'{filepath}' has extension: '{extension}'")

        if self.mime:
            # Return MIME type for extension
            if extension in self.extension_mime_map:
                result = self.extension_mime_map[extension]
                self.debug_print(f"Extension '{extension}' mapped to MIME: {result}")
                return result
        else:
            # Return human-readable type for extension
            if extension in self.extension_map:
                result = self.extension_map[extension]
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

            # Return MIME type or readable format based on mode
            if self.mime:
                # In MIME mode, return just the MIME type
                if mime_type:
                    self.debug_print(f"Magic MIME result for '{filepath}': {mime_type}")
                    return mime_type
            else:
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
                    self.debug_print(
                        f"Magic test result for '{filepath}': {description}"
                    )
                    return description

        except Exception as e:
            self.debug_print(f"Magic test failed for '{filepath}': {e}")
            # Fallback to Python's mimetypes module
            mime_type, _ = mimetypes.guess_type(filepath)
            if mime_type is not None:
                if self.mime:
                    self.debug_print(
                        f"Fallback MIME result for '{filepath}': {mime_type}"
                    )
                    return mime_type
                else:
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
                    "text/x-python",
                ),
                (
                    r"#!/bin/bash|#!/bin/sh|^#\s*bash|^#\s*shell",
                    "shell script",
                    "text/x-shellscript",
                ),
                (
                    r"^#!/usr/bin/env node|^const\s+\w+|^let\s+\w+|^var\s+\w+",
                    "JavaScript file",
                    "text/javascript",
                ),
                (
                    r'^#include\s*<.*>|^#include\s*".*"|int\s+main\s*\(',
                    "C/C++ source",
                    "text/x-c",
                ),
                (
                    r"^package\s+\w+|^public\s+class\s+\w+|^import\s+java\.",
                    "Java source",
                    "text/x-java-source",
                ),
                (r"^<\?php|<\?=|\$\w+\s*=", "PHP script", "text/x-php"),
                (
                    r"^class\s+\w+|^def\s+\w+|^module\s+\w+",
                    "Ruby script",
                    "text/x-ruby",
                ),
                (
                    r"^<!DOCTYPE html|^<html|^<head>|^<body>",
                    "HTML document",
                    "text/html",
                ),
                (r'^\s*{|\s*"[\w-]+"\s*:', "JSON data", "application/json"),
                (r"^<\?xml|^<[a-zA-Z][^>]*>", "XML document", "application/xml"),
                (
                    r"^\s*[\w-]+\s*:\s*[\w-]+|^\s*\.|^\s*#[a-zA-Z]",
                    "CSS stylesheet",
                    "text/css",
                ),
                (
                    r"^#+\s+\w+|^\*\s+\w+|^\d+\.\s+\w+",
                    "Markdown document",
                    "text/markdown",
                ),
            ]

            for pattern, file_type, mime_type in patterns:
                if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                    if self.mime:
                        self.debug_print(
                            f"Pattern '{pattern}' matched for '{filepath}', "
                            f"detected MIME: {mime_type}"
                        )
                        return mime_type
                    else:
                        self.debug_print(
                            f"Pattern '{pattern}' matched for '{filepath}', "
                            f"detected as: {file_type}"
                        )
                        return file_type

            # Check if it's mostly text
            printable_chars = sum(1 for c in content if c.isprintable() or c.isspace())
            if len(content) > 0:
                printable_ratio = printable_chars / len(content)
                self.debug_print(
                    f"Printable character ratio for '{filepath}': "
                    f"{printable_ratio:.2f}"
                )
                if printable_ratio > 0.7:
                    if self.mime:
                        self.debug_print(
                            f"'{filepath}' detected as text/plain based on "
                            f"printable character ratio"
                        )
                        return "text/plain"
                    else:
                        self.debug_print(
                            f"'{filepath}' detected as text file based on "
                            f"printable character ratio"
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

        # Check existence, but allow broken symlinks if no_dereference is True
        path = Path(filepath)
        if not os.path.exists(filepath) and not (
            self.no_dereference and path.is_symlink()
        ):
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
        unknown_type = "application/octet-stream" if self.mime else "unknown file type"
        if verbose:
            return unknown_type, "None"
        else:
            return unknown_type, None


def read_files_from_namefile(namefile, debug=False, exit_on_error=False):
    """Read filenames from a namefile, one per line"""
    files = []
    if debug:
        print(f"DEBUG: Reading filenames from '{namefile}'", file=sys.stderr)

    try:
        if namefile == "-":
            # Read from stdin
            if debug:
                print("DEBUG: Reading filenames from stdin", file=sys.stderr)
            for line in sys.stdin:
                filename = line.strip()
                if filename:  # Skip empty lines
                    files.append(filename)
                    if debug:
                        print(f"DEBUG: Added '{filename}' from stdin", file=sys.stderr)
        else:
            # Read from file
            with open(namefile, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    filename = line.strip()
                    if filename:  # Skip empty lines
                        files.append(filename)
                        if debug:
                            print(
                                f"DEBUG: Added '{filename}' from {namefile}:{line_num}",
                                file=sys.stderr,
                            )
                    elif debug:
                        print(
                            f"DEBUG: Skipped empty line {line_num} in '{namefile}'",
                            file=sys.stderr,
                        )
    except (IOError, OSError) as e:
        error_msg = f"ERROR: Cannot read namefile '{namefile}': {e}"
        if exit_on_error:
            print(error_msg, file=sys.stderr)
            sys.exit(1)
        else:
            print(error_msg)
            if debug:
                print(f"DEBUG: {error_msg}", file=sys.stderr)
            return []

    if debug:
        print(f"DEBUG: Read {len(files)} filenames from '{namefile}'", file=sys.stderr)
    return files


def main():
    # Custom argument processing to handle files-from in order
    import sys

    # Parse arguments manually to handle files-from processing in order
    argv = sys.argv[1:]  # Skip program name

    # Default values
    verbose = False
    brief = False
    mime = False
    debug = False
    exit_on_error = False
    extension = False
    separator = ":"
    no_dereference = None  # Will be set based on POSIXLY_CORRECT if not specified
    remaining_files = []
    any_files_processed = False

    # Initialize the tester early so it can be used in file processing
    tester = FileTypeTester(debug=debug, no_dereference=no_dereference, mime=mime)

    def process_files_with_current_settings(files_to_process):
        """Process files immediately with current settings"""
        nonlocal any_files_processed

        for filepath in files_to_process:
            any_files_processed = True
            path = Path(filepath)

            # Check if the path exists at all (but handle symlinks specially)
            if not path.exists() and not path.is_symlink():
                error_msg = f"ERROR: File or directory '{filepath}' does not exist"
                if exit_on_error:
                    print(error_msg, file=sys.stderr)
                    sys.exit(1)
                else:
                    print(f"{filepath}{separator} {error_msg}")
                    continue

            # Check if it's a directory, but handle symlinks specially
            if path.is_dir() and not (path.is_symlink() and tester.no_dereference):
                if debug:
                    print(
                        f"DEBUG: '{filepath}' is a directory, processing recursively",
                        file=sys.stderr,
                    )
                # Process directory recursively
                files_in_dir = get_files_from_directory(filepath)
                if files_in_dir:
                    if debug:
                        print(
                            f"DEBUG: Found {len(files_in_dir)} files in directory "
                            f"'{filepath}', sorting...",
                            file=sys.stderr,
                        )
                    for file_in_dir in sorted(files_in_dir):
                        process_single_file(file_in_dir)
                else:
                    if debug:
                        print(
                            f"DEBUG: Directory '{filepath}' is empty or inaccessible",
                            file=sys.stderr,
                        )
                    print(f"{filepath}{separator} directory (empty or inaccessible)")
            else:
                if debug:
                    print(
                        f"DEBUG: '{filepath}' is a file, processing directly",
                        file=sys.stderr,
                    )
                # Process single file
                process_single_file(filepath)

    def process_single_file(filepath):
        """Process a single file and output the result"""
        file_type, test_category = tester.detect_file_type(filepath, verbose=verbose)

        # Check for errors and exit if -E flag is enabled
        if exit_on_error and file_type.startswith("ERROR:"):
            print(file_type, file=sys.stderr)
            sys.exit(1)

        if extension:
            # Extension mode: show extensions for the file type
            extensions = tester.get_extensions_for_type(file_type)
            if extensions:
                if brief:
                    print(extensions)
                else:
                    print(f"{filepath}{separator} {extensions}")
            else:
                if brief:
                    print("")
                else:
                    print(f"{filepath}{separator} ")
        elif brief:
            # Brief mode: only output the file type
            print(file_type)
        elif verbose and test_category:
            # Verbose mode: include test category
            print(f"{filepath}{separator} {file_type} [{test_category} test]")
        else:
            # Default mode: filename and file type
            print(f"{filepath}{separator} {file_type}")

    def get_files_from_directory(directory_path):
        """Recursively get all files from a directory"""
        if debug:
            print(
                f"DEBUG: Scanning directory '{directory_path}' for files",
                file=sys.stderr,
            )
        files = []
        try:
            for root, dirs, filenames in os.walk(directory_path):
                if debug:
                    print(
                        f"DEBUG: Found {len(filenames)} files in '{root}'",
                        file=sys.stderr,
                    )
                for filename in filenames:
                    full_path = os.path.join(root, filename)
                    files.append(full_path)
                    if debug:
                        print(
                            f"DEBUG: Added file '{full_path}' to processing list",
                            file=sys.stderr,
                        )
        except (OSError, PermissionError) as e:
            error_msg = f"ERROR: Cannot access directory '{directory_path}': {e}"
            if exit_on_error:
                print(error_msg, file=sys.stderr)
                sys.exit(1)
            else:
                print(error_msg)
                if debug:
                    print(f"DEBUG: {error_msg}", file=sys.stderr)
        return files

    i = 0
    while i < len(argv):
        arg = argv[i]

        if arg == "--help":
            # Show help and exit
            parser = argparse.ArgumentParser(
                description=(
                    "FFT - File Type Tester: Determine file types using filesystem, "
                    "magic, and language tests"
                ),
                add_help=False,  # Disable automatic help to use -h for no-dereference
            )
            parser.add_argument(
                "files", nargs="*", help="Files or directories to analyze"
            )
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
                help=(
                    "Recursively process directories "
                    "(default when directory is given)"
                ),
            )
            parser.add_argument(
                "-d",
                "--debug",
                action="store_true",
                help="Print internal debugging information to stderr",
            )
            parser.add_argument(
                "-E",
                "--exit-on-error",
                action="store_true",
                help="Exit immediately on filesystem errors instead of continuing",
            )
            parser.add_argument(
                "--extension",
                action="store_true",
                help=(
                    "Print a slash-separated list of valid extensions "
                    "for the file type found"
                ),
            )
            parser.add_argument(
                "-F",
                "--separator",
                default=":",
                help=(
                    "Use the specified string as the separator between "
                    "the filename and the file result (default: ':')"
                ),
            )
            parser.add_argument(
                "-f",
                "--files-from",
                metavar="namefile",
                help=(
                    "Read the names of the files to be examined from namefile "
                    "(one per line) before the argument list"
                ),
            )
            parser.add_argument(
                "-h",
                "--no-dereference",
                action="store_true",
                help=(
                    "This option causes symlinks not to be followed "
                    "(on systems that support symbolic links). "
                    "This is the default if the environment variable "
                    "POSIXLY_CORRECT is not defined."
                ),
            )
            parser.add_argument(
                "-i",
                "--mime",
                action="store_true",
                help=(
                    "Causes the file command to output mime type strings "
                    "rather than the more traditional human readable ones. "
                    "Thus it may say 'text/plain; charset=us-ascii' rather "
                    "than 'ASCII text'."
                ),
            )
            parser.add_argument(
                "--version",
                action="version",
                version=f"%(prog)s {__version__}",
                help="Show version information",
            )
            parser.add_argument(
                "--help",
                action="help",
                help="Show this help message and exit",
            )
            parser.print_help()
            sys.exit(0)
        elif arg == "--version":
            print(f"fft {__version__}")
            sys.exit(0)
        elif arg in ["-v", "--verbose"]:
            verbose = True
        elif arg in ["-b", "--brief"]:
            brief = True
        elif arg in ["-r", "--recursive"]:
            pass  # Recursive is default behavior for directories
        elif arg in ["-d", "--debug"]:
            debug = True
            # Update tester debug setting
            tester = FileTypeTester(
                debug=debug, no_dereference=no_dereference, mime=mime
            )
        elif arg in ["-E", "--exit-on-error"]:
            exit_on_error = True
        elif arg in ["-h", "--no-dereference"]:
            no_dereference = True
            # Update tester no_dereference setting
            tester = FileTypeTester(
                debug=debug, no_dereference=no_dereference, mime=mime
            )
        elif arg in ["-i", "--mime"]:
            mime = True
            # Update tester mime setting
            tester = FileTypeTester(
                debug=debug, no_dereference=no_dereference, mime=mime
            )
        elif arg == "--extension":
            extension = True
        elif arg in ["-F", "--separator"]:
            if i + 1 >= len(argv):
                print(f"Error: {arg} requires an argument", file=sys.stderr)
                sys.exit(2)
            separator = argv[i + 1]
            i += 1  # Skip the separator value
        elif arg in ["-f", "--files-from"]:
            if i + 1 >= len(argv):
                print(f"Error: {arg} requires an argument", file=sys.stderr)
                sys.exit(2)
            namefile = argv[i + 1]
            i += 1  # Skip the namefile value

            # Process files-from immediately with current settings
            files_from_namefile = read_files_from_namefile(
                namefile, debug, exit_on_error
            )
            if debug:
                print(
                    f"DEBUG: Processing {len(files_from_namefile)} files "
                    f"from '{namefile}' with separator '{separator}'",
                    file=sys.stderr,
                )
            process_files_with_current_settings(files_from_namefile)
        elif arg.startswith("-"):
            print(f"Error: Unknown option {arg}", file=sys.stderr)
            sys.exit(2)
        else:
            # Regular file argument - save for later processing
            remaining_files.append(arg)

        i += 1

    # Process any remaining command line file arguments
    if remaining_files:
        if debug:
            print(
                f"DEBUG: Processing {len(remaining_files)} remaining command line "
                f"files with separator '{separator}'",
                file=sys.stderr,
            )
        process_files_with_current_settings(remaining_files)
        any_files_processed = True

    # Validate that we processed at least one file
    if not any_files_processed:
        print(
            "Error: Either namefile or at least one filename argument must be present",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
