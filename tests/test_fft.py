# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Brandon Perkins <bdperkin@gmail.com>

"""Tests for FFT (File Type Tester)."""

import os
import tempfile
import unittest.mock
from pathlib import Path

import pytest

import fft


class TestFileTypeTester:
    """Test cases for the FileTypeTester class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.tester = fft.FileTypeTester()

    def test_init(self):
        """Test FileTypeTester initialization."""
        assert hasattr(self.tester, "mime_detector")
        assert hasattr(self.tester, "description_detector")

    def test_filesystem_tests_nonexistent_file(self):
        """Test filesystem tests with non-existent file."""
        # Filesystem tests check extension even for non-existent files
        result = self.tester.filesystem_tests("/nonexistent/file.txt")
        assert result == "text file"

        # Test with unknown extension
        result = self.tester.filesystem_tests("/nonexistent/file.unknown")
        assert result is None

    def test_filesystem_tests_directory(self):
        """Test filesystem tests with directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.tester.filesystem_tests(tmpdir)
            assert result == "directory"

    def test_filesystem_tests_symlink(self):
        """Test filesystem tests with symbolic link."""
        with tempfile.TemporaryDirectory() as tmpdir:
            target_file = os.path.join(tmpdir, "target.txt")
            link_file = os.path.join(tmpdir, "link.txt")

            # Create target file and symlink
            Path(target_file).touch()
            os.symlink(target_file, link_file)

            result = self.tester.filesystem_tests(link_file)
            assert result == "symbolic link"

    def test_filesystem_tests_executable_script(self):
        """Test filesystem tests with executable script."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("#!/usr/bin/env python3\nprint('hello')")
            f.flush()

            # Make file executable
            os.chmod(f.name, 0o755)

            result = self.tester.filesystem_tests(f.name)
            assert result == "executable script"

            os.unlink(f.name)

    def test_filesystem_tests_executable_file(self):
        """Test filesystem tests with executable file (no shebang)."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("binary content")
            f.flush()

            # Make file executable
            os.chmod(f.name, 0o755)

            result = self.tester.filesystem_tests(f.name)
            assert result == "executable file"

            os.unlink(f.name)

    def test_filesystem_tests_extensions(self):
        """Test filesystem tests with various file extensions."""
        test_cases = [
            ("file.py", "Python script"),
            ("file.js", "JavaScript file"),
            ("file.html", "HTML document"),
            ("file.css", "CSS stylesheet"),
            ("file.json", "JSON data"),
            ("file.md", "Markdown document"),
            ("file.txt", "text file"),
            ("file.jpg", "JPEG image"),
            ("file.png", "PNG image"),
            ("file.pdf", "PDF document"),
            ("file.zip", "ZIP archive"),
            ("file.unknown", None),
        ]

        for filename, expected in test_cases:
            with tempfile.NamedTemporaryFile(suffix=filename, delete=False) as f:
                f.write(b"test content")
                f.flush()

                result = self.tester.filesystem_tests(f.name)
                assert (
                    result == expected
                ), f"Failed for {filename}: expected {expected}, got {result}"

                os.unlink(f.name)

    def test_magic_tests_with_mock(self):
        """Test magic tests with mocked magic library."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("test content")
            f.flush()

            # Mock the magic detectors
            with unittest.mock.patch.object(
                self.tester.mime_detector, "from_file", return_value="text/plain"
            ):
                with unittest.mock.patch.object(
                    self.tester.description_detector,
                    "from_file",
                    return_value="ASCII text",
                ):
                    result = self.tester.magic_tests(f.name)
                    assert result == "ASCII text (text/plain)"

            os.unlink(f.name)

    def test_magic_tests_exception_handling(self):
        """Test magic tests exception handling."""
        with unittest.mock.patch.object(
            self.tester.mime_detector, "from_file", side_effect=Exception("Mock error")
        ):
            with unittest.mock.patch.object(
                self.tester.description_detector,
                "from_file",
                side_effect=Exception("Mock error"),
            ):
                with unittest.mock.patch(
                    "mimetypes.guess_type", return_value=("text/plain", None)
                ):
                    result = self.tester.magic_tests("dummy_file")
                    assert result == "file of type text/plain"

    def test_language_tests_python(self):
        """Test language detection for Python files."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("#!/usr/bin/env python3\nimport os\nprint('hello')")
            f.flush()

            result = self.tester.language_tests(f.name)
            assert result == "Python script"

            os.unlink(f.name)

    def test_language_tests_javascript(self):
        """Test language detection for JavaScript files."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".js") as f:
            f.write("const hello = 'world';\nconsole.log(hello);")
            f.flush()

            result = self.tester.language_tests(f.name)
            assert result == "JavaScript file"

            os.unlink(f.name)

    def test_language_tests_html(self):
        """Test language detection for HTML files."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html") as f:
            f.write("<!DOCTYPE html>\n<html><head><title>Test</title></head></html>")
            f.flush()

            result = self.tester.language_tests(f.name)
            assert result == "HTML document"

            os.unlink(f.name)

    def test_language_tests_json(self):
        """Test language detection for JSON files."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            f.write('{"name": "test", "value": 123}')
            f.flush()

            result = self.tester.language_tests(f.name)
            assert result == "JSON data"

            os.unlink(f.name)

    def test_language_tests_markdown(self):
        """Test language detection for Markdown files."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md") as f:
            f.write("# Test Header\n\nThis is a test markdown file.")
            f.flush()

            result = self.tester.language_tests(f.name)
            assert result == "Markdown document"

            os.unlink(f.name)

    def test_language_tests_text_file(self):
        """Test language detection for generic text files."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("This is just plain text content without any special patterns.")
            f.flush()

            result = self.tester.language_tests(f.name)
            assert result == "text file"

            os.unlink(f.name)

    def test_language_tests_binary_file(self):
        """Test language detection for binary files."""
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            f.write(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09")
            f.flush()

            result = self.tester.language_tests(f.name)
            assert result is None

            os.unlink(f.name)

    def test_detect_file_type_nonexistent(self):
        """Test detect_file_type with non-existent file."""
        result, test_category = self.tester.detect_file_type("/nonexistent/file.txt")
        assert "ERROR" in result
        assert test_category is None

    def test_detect_file_type_verbose(self):
        """Test detect_file_type with verbose mode."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("print('hello')")
            f.flush()

            result, test_category = self.tester.detect_file_type(f.name, verbose=True)
            assert result == "Python script"
            assert test_category == "Filesystem"

            os.unlink(f.name)

    def test_detect_file_type_fallback(self):
        """Test detect_file_type fallback to unknown."""
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            f.write(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09")
            f.flush()

            # Mock all detection methods to return None
            with unittest.mock.patch.object(
                self.tester, "filesystem_tests", return_value=None
            ):
                with unittest.mock.patch.object(
                    self.tester, "magic_tests", return_value=None
                ):
                    with unittest.mock.patch.object(
                        self.tester, "language_tests", return_value=None
                    ):
                        result, test_category = self.tester.detect_file_type(
                            f.name, verbose=True
                        )
                        assert result == "unknown file type"
                        assert test_category == "None"

            os.unlink(f.name)


class TestMain:
    """Test cases for the main function."""

    def test_main_help(self, capsys):
        """Test main function with help argument."""
        import sys

        # Mock sys.argv to simulate --help
        with unittest.mock.patch.object(sys, "argv", ["fft.py", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                fft.main()

            assert exc_info.value.code == 0
            captured = capsys.readouterr()
            assert "FFT - File Type Tester" in captured.out
            assert "--brief" in captured.out
            assert "--verbose" in captured.out

    def test_main_version(self, capsys):
        """Test main function with version argument."""
        import sys

        # Mock sys.argv to simulate --version
        with unittest.mock.patch.object(sys, "argv", ["fft.py", "--version"]):
            with pytest.raises(SystemExit) as exc_info:
                fft.main()

            assert exc_info.value.code == 0
            captured = capsys.readouterr()
            assert fft.__version__ in captured.out

    def test_main_brief_mode(self, capsys):
        """Test main function with brief mode."""
        import sys

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("print('hello')")
            f.flush()

            # Mock sys.argv to simulate brief mode
            with unittest.mock.patch.object(sys, "argv", ["fft.py", "--brief", f.name]):
                fft.main()

            captured = capsys.readouterr()
            assert (
                f.name not in captured.out
            )  # Filename should not appear in brief mode
            assert "Python script" in captured.out

            os.unlink(f.name)

    def test_main_verbose_mode(self, capsys):
        """Test main function with verbose mode."""
        import sys

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("print('hello')")
            f.flush()

            # Mock sys.argv to simulate verbose mode
            with unittest.mock.patch.object(
                sys, "argv", ["fft.py", "--verbose", f.name]
            ):
                fft.main()

            captured = capsys.readouterr()
            assert f.name in captured.out  # Filename should appear
            assert "Python script" in captured.out
            assert "[Filesystem test]" in captured.out

            os.unlink(f.name)

    def test_main_default_mode(self, capsys):
        """Test main function with default mode."""
        import sys

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("print('hello')")
            f.flush()

            # Mock sys.argv to simulate default mode
            with unittest.mock.patch.object(sys, "argv", ["fft.py", f.name]):
                fft.main()

            captured = capsys.readouterr()
            assert f.name in captured.out  # Filename should appear
            assert "Python script" in captured.out
            assert "[Filesystem test]" not in captured.out  # No test category

            os.unlink(f.name)

    def test_main_multiple_files(self, capsys):
        """Test main function with multiple files."""
        import sys

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f1:
            f1.write("print('hello')")
            f1.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".js"
            ) as f2:
                f2.write("console.log('hello');")
                f2.flush()

                # Mock sys.argv to simulate multiple files
                with unittest.mock.patch.object(
                    sys, "argv", ["fft.py", f1.name, f2.name]
                ):
                    fft.main()

                captured = capsys.readouterr()
                assert "Python script" in captured.out
                assert "JavaScript file" in captured.out

                os.unlink(f2.name)

            os.unlink(f1.name)


@pytest.mark.integration
class TestIntegration:
    """Integration tests for the FFT tool."""

    def test_real_files_detection(self):
        """Test detection on real project files."""
        tester = fft.FileTypeTester()

        # Test the main Python file
        if os.path.exists("fft.py"):
            result, _ = tester.detect_file_type("fft.py")
            assert "Python" in result or "executable script" in result

        # Test the pyproject.toml file
        if os.path.exists("pyproject.toml"):
            result, _ = tester.detect_file_type("pyproject.toml")
            assert result is not None

        # Test the README.md file
        if os.path.exists("README.md"):
            result, _ = tester.detect_file_type("README.md")
            assert "Markdown" in result or "text" in result
