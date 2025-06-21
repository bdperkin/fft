#!/usr/bin/env python3
"""
FFT - File Type Tester
Determines the file type of files using filesystem, magic, and language tests.
"""

import sys
import os
import argparse
import mimetypes
import magic
import re
from pathlib import Path


class FileTypeTester:
    def __init__(self):
        self.mime_detector = magic.Magic(magic.MAGIC_MIME_TYPE)
        self.description_detector = magic.Magic(magic.MAGIC_NONE)
        
    def filesystem_tests(self, filepath):
        """
        Filesystem-based tests: check extension, permissions, special files
        """
        path = Path(filepath)
        
        # Check if it's a directory
        if path.is_dir():
            return "directory"
            
        # Check if it's a symbolic link
        if path.is_symlink():
            return "symbolic link"
            
        # Check if it's a block or character device
        if path.is_block_device():
            return "block device"
        if path.is_char_device():
            return "character device"
            
        # Check if it's a FIFO or socket
        if path.is_fifo():
            return "FIFO (named pipe)"
        if path.is_socket():
            return "socket"
            
        # Check executable permissions
        if os.access(filepath, os.X_OK) and path.is_file():
            # Check if it starts with shebang
            try:
                with open(filepath, 'rb') as f:
                    first_bytes = f.read(2)
                    if first_bytes == b'#!':
                        return "executable script"
            except (IOError, OSError):
                pass
            return "executable file"
            
        # Check common extensions
        extension = path.suffix.lower()
        extension_map = {
            '.txt': 'text file',
            '.py': 'Python script',
            '.js': 'JavaScript file',
            '.html': 'HTML document',
            '.css': 'CSS stylesheet',
            '.json': 'JSON data',
            '.xml': 'XML document',
            '.csv': 'CSV data',
            '.md': 'Markdown document',
            '.jpg': 'JPEG image',
            '.jpeg': 'JPEG image',
            '.png': 'PNG image',
            '.gif': 'GIF image',
            '.pdf': 'PDF document',
            '.zip': 'ZIP archive',
            '.tar': 'TAR archive',
            '.gz': 'GZIP compressed file',
            '.exe': 'Windows executable',
            '.dll': 'Windows DLL',
            '.so': 'shared library',
            '.a': 'static library',
            '.o': 'object file',
            '.c': 'C source file',
            '.cpp': 'C++ source file',
            '.h': 'C/C++ header file',
            '.java': 'Java source file',
            '.class': 'Java bytecode',
            '.rb': 'Ruby script',
            '.php': 'PHP script',
            '.sh': 'shell script',
            '.bat': 'batch file',
            '.ps1': 'PowerShell script',
        }
        
        if extension in extension_map:
            return extension_map[extension]
            
        return None
        
    def magic_tests(self, filepath):
        """
        Magic number tests using libmagic
        """
        try:
            # Get MIME type
            mime_type = self.mime_detector.from_file(filepath)
            
            # Get file description
            description = self.description_detector.from_file(filepath)
            
            # Return a more readable format
            if mime_type and description:
                return f"{description} ({mime_type})"
            elif mime_type:
                return f"file of type {mime_type}"
            elif description:
                return description
                
        except Exception as e:
            # Fallback to Python's mimetypes module
            mime_type, _ = mimetypes.guess_type(filepath)
            if mime_type:
                return f"file of type {mime_type}"
                
        return None
        
    def language_tests(self, filepath):
        """
        Language detection tests based on file content analysis
        """
        try:
            # Try to read the file as text
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1024)  # Read first 1KB
                
            # Check for specific language patterns
            patterns = [
                (r'#!/usr/bin/env python|#!/usr/bin/python|^import\s+\w+|^from\s+\w+\s+import', 'Python script'),
                (r'#!/bin/bash|#!/bin/sh|^#\s*bash|^#\s*shell', 'shell script'),
                (r'^#!/usr/bin/env node|^const\s+\w+|^let\s+\w+|^var\s+\w+', 'JavaScript file'),
                (r'^#include\s*<.*>|^#include\s*".*"|int\s+main\s*\(', 'C/C++ source'),
                (r'^package\s+\w+|^public\s+class\s+\w+|^import\s+java\.', 'Java source'),
                (r'^<\?php|<\?=|\$\w+\s*=', 'PHP script'),
                (r'^class\s+\w+|^def\s+\w+|^module\s+\w+', 'Ruby script'),
                (r'^<!DOCTYPE html|^<html|^<head>|^<body>', 'HTML document'),
                (r'^\s*{|\s*"[\w-]+"\s*:', 'JSON data'),
                (r'^<\?xml|^<[a-zA-Z][^>]*>', 'XML document'),
                (r'^\s*[\w-]+\s*:\s*[\w-]+|^\s*\.|^\s*#[a-zA-Z]', 'CSS stylesheet'),
                (r'^#+\s+\w+|^\*\s+\w+|^\d+\.\s+\w+', 'Markdown document'),
            ]
            
            for pattern, file_type in patterns:
                if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                    return file_type
                    
            # Check if it's mostly text
            printable_chars = sum(1 for c in content if c.isprintable() or c.isspace())
            if len(content) > 0 and printable_chars / len(content) > 0.7:
                return "text file"
                
        except (UnicodeDecodeError, IOError, OSError):
            pass
            
        return None
        
    def detect_file_type(self, filepath):
        """
        Main detection method that runs tests in order
        """
        if not os.path.exists(filepath):
            return f"ERROR: File '{filepath}' does not exist"
            
        # Run tests in order
        tests = [
            ("Filesystem", self.filesystem_tests),
            ("Magic", self.magic_tests),
            ("Language", self.language_tests),
        ]
        
        for test_name, test_func in tests:
            try:
                result = test_func(filepath)
                if result:
                    return result
            except Exception as e:
                # Continue to next test if current one fails
                continue
                
        return "unknown file type"


def main():
    parser = argparse.ArgumentParser(
        description='FFT - File Type Tester: Determine file types using filesystem, magic, and language tests'
    )
    parser.add_argument('files', nargs='+', help='Files to analyze')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize the tester
    tester = FileTypeTester()
    
    # Process each file
    for filepath in args.files:
        file_type = tester.detect_file_type(filepath)
        
        if args.verbose:
            print(f"{filepath}: {file_type}")
        else:
            print(file_type)


if __name__ == '__main__':
    main() 