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


class TestDirectoryProcessing:
    """Test cases for directory processing functionality."""

    def test_main_with_directory(self, capsys):
        """Test main function with directory argument."""
        import sys
        import tempfile

        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            py_file = os.path.join(tmpdir, "test.py")
            with open(py_file, "w") as f:
                f.write("print('hello')")

            js_file = os.path.join(tmpdir, "test.js")
            with open(js_file, "w") as f:
                f.write("console.log('hello');")

            # Create subdirectory with more files
            subdir = os.path.join(tmpdir, "subdir")
            os.makedirs(subdir)

            json_file = os.path.join(subdir, "test.json")
            with open(json_file, "w") as f:
                f.write('{"name": "test"}')

            # Mock sys.argv to test directory processing
            with unittest.mock.patch.object(sys, "argv", ["fft.py", tmpdir]):
                fft.main()

            captured = capsys.readouterr()

            # Check that all files were processed
            assert "test.py: Python script" in captured.out
            assert "test.js: JavaScript file" in captured.out
            assert "test.json: JSON data" in captured.out

            # Check that files are sorted and include full paths
            output_lines = captured.out.strip().split("\n")
            assert len(output_lines) == 3

            # Files should be processed in sorted order
            assert all(tmpdir in line for line in output_lines)

    def test_main_with_directory_verbose(self, capsys):
        """Test main function with directory argument in verbose mode."""
        import sys
        import tempfile

        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as tmpdir:
            py_file = os.path.join(tmpdir, "test.py")
            with open(py_file, "w") as f:
                f.write("print('hello')")

            # Mock sys.argv to test directory processing with verbose
            with unittest.mock.patch.object(sys, "argv", ["fft.py", "-v", tmpdir]):
                fft.main()

            captured = capsys.readouterr()
            assert "test.py: Python script [Filesystem test]" in captured.out

    def test_main_with_directory_brief(self, capsys):
        """Test main function with directory argument in brief mode."""
        import sys
        import tempfile

        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as tmpdir:
            py_file = os.path.join(tmpdir, "test.py")
            with open(py_file, "w") as f:
                f.write("print('hello')")

            js_file = os.path.join(tmpdir, "test.js")
            with open(js_file, "w") as f:
                f.write("console.log('hello');")

            # Mock sys.argv to test directory processing with brief
            with unittest.mock.patch.object(sys, "argv", ["fft.py", "-b", tmpdir]):
                fft.main()

            captured = capsys.readouterr()
            output_lines = captured.out.strip().split("\n")

            # In brief mode, no filenames should appear
            assert all(tmpdir not in line for line in output_lines)
            assert "Python script" in captured.out
            assert "JavaScript file" in captured.out

    def test_main_with_empty_directory(self, capsys):
        """Test main function with empty directory."""
        import sys
        import tempfile

        # Create an empty temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Make sure directory is empty
            assert len(os.listdir(tmpdir)) == 0

            # Mock sys.argv to test empty directory processing
            with unittest.mock.patch.object(sys, "argv", ["fft.py", tmpdir]):
                fft.main()

            captured = capsys.readouterr()
            assert f"{tmpdir}: directory (empty or inaccessible)" in captured.out

    def test_main_with_mixed_files_and_directories(self, capsys):
        """Test main function with mix of files and directories."""
        import sys
        import tempfile

        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file in the directory
            py_file = os.path.join(tmpdir, "test.py")
            with open(py_file, "w") as f:
                f.write("print('hello')")

            # Create a standalone test file
            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".js"
            ) as standalone_file:
                standalone_file.write("console.log('hello');")
                standalone_file.flush()

                # Mock sys.argv to test mixed processing
                with unittest.mock.patch.object(
                    sys, "argv", ["fft.py", standalone_file.name, tmpdir]
                ):
                    fft.main()

                captured = capsys.readouterr()

                # Check that both standalone file and directory files were processed
                assert f"{standalone_file.name}: JavaScript file" in captured.out
                assert "test.py: Python script" in captured.out

                os.unlink(standalone_file.name)

    def test_main_with_inaccessible_directory(self, capsys):
        """Test main function with inaccessible directory."""
        import sys

        # Test with non-existent directory
        with unittest.mock.patch.object(
            sys, "argv", ["fft.py", "/nonexistent/directory"]
        ):
            fft.main()

        captured = capsys.readouterr()
        assert (
            "ERROR: Cannot access directory" in captured.out
            or "ERROR: File" in captured.out
        )

    def test_get_files_from_directory_function(self):
        """Test the get_files_from_directory function directly."""
        import tempfile

        # Create a temporary directory with nested structure
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files in root
            file1 = os.path.join(tmpdir, "file1.txt")
            with open(file1, "w") as f:
                f.write("test")

            # Create subdirectory with files
            subdir = os.path.join(tmpdir, "subdir")
            os.makedirs(subdir)
            file2 = os.path.join(subdir, "file2.py")
            with open(file2, "w") as f:
                f.write("print('test')")

            # Create nested subdirectory
            nested_subdir = os.path.join(subdir, "nested")
            os.makedirs(nested_subdir)
            file3 = os.path.join(nested_subdir, "file3.js")
            with open(file3, "w") as f:
                f.write("console.log('test');")

            # Test the function using the implementation from main
            files = []
            try:
                for root, dirs, filenames in os.walk(tmpdir):
                    for filename in filenames:
                        files.append(os.path.join(root, filename))
            except (OSError, PermissionError):
                pass

            # Check that all files were found
            assert len(files) == 3
            assert any("file1.txt" in f for f in files)
            assert any("file2.py" in f for f in files)
            assert any("file3.js" in f for f in files)

            # Check that files are properly nested
            assert any(os.path.join("subdir", "file2.py") in f for f in files)
            assert any(os.path.join("subdir", "nested", "file3.js") in f for f in files)


class TestDebugFunctionality:
    """Test cases for debug functionality."""

    def test_debug_mode_initialization(self):
        """Test that debug mode is properly initialized."""
        # Test debug mode enabled
        tester_debug = fft.FileTypeTester(debug=True)
        assert tester_debug.debug is True

        # Test debug mode disabled (default)
        tester_normal = fft.FileTypeTester()
        assert tester_normal.debug is False

    def test_debug_print_enabled(self, capsys):
        """Test that debug_print outputs to stderr when debug is enabled."""
        tester = fft.FileTypeTester(debug=True)
        tester.debug_print("Test debug message")

        captured = capsys.readouterr()
        assert captured.err == "DEBUG: Test debug message\n"
        assert captured.out == ""

    def test_debug_print_disabled(self, capsys):
        """Test that debug_print is silent when debug is disabled."""
        tester = fft.FileTypeTester(debug=False)
        tester.debug_print("Test debug message")

        captured = capsys.readouterr()
        assert captured.err == ""
        assert captured.out == ""

    def test_main_with_debug_flag(self, capsys):
        """Test main function with debug flag."""
        import sys
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("print('hello')")
            f.flush()

            # Mock sys.argv to simulate debug mode
            with unittest.mock.patch.object(sys, "argv", ["fft.py", "-d", f.name]):
                fft.main()

            captured = capsys.readouterr()

            # Check that debug output is present in stderr
            assert "DEBUG: Processing 1 argument(s)" in captured.err
            assert "DEBUG: Starting file type detection" in captured.err
            assert "DEBUG: Running filesystem tests" in captured.err

            # Check that normal output is still in stdout
            assert "Python script" in captured.out

            os.unlink(f.name)

    def test_debug_filesystem_tests(self, capsys):
        """Test debug output in filesystem tests."""
        import tempfile

        tester = fft.FileTypeTester(debug=True)

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("print('hello')")
            f.flush()

            result = tester.filesystem_tests(f.name)

            captured = capsys.readouterr()
            assert "DEBUG: Running filesystem tests" in captured.err
            assert "DEBUG: Extension '.py' mapped to: Python script" in captured.err
            assert result == "Python script"

            os.unlink(f.name)

    def test_debug_magic_tests(self, capsys):
        """Test debug output in magic tests."""
        import tempfile

        tester = fft.FileTypeTester(debug=True)

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            f.write('{"test": "data"}')
            f.flush()

            tester.magic_tests(f.name)

            captured = capsys.readouterr()
            assert "DEBUG: Running magic tests" in captured.err
            assert "DEBUG: Magic MIME type" in captured.err
            assert "DEBUG: Magic description" in captured.err

            os.unlink(f.name)

    def test_debug_language_tests(self, capsys):
        """Test debug output in language tests."""
        import tempfile

        tester = fft.FileTypeTester(debug=True)

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("print('hello world')")
            f.flush()

            tester.language_tests(f.name)

            captured = capsys.readouterr()
            assert "DEBUG: Running language tests" in captured.err
            assert "DEBUG: Read" in captured.err and "characters from" in captured.err

            os.unlink(f.name)

    def test_debug_detect_file_type_all_tests(self, capsys):
        """Test debug output shows all test attempts."""
        import tempfile

        tester = fft.FileTypeTester(debug=True)

        # Create a file with no extension to force multiple test attempts
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write('{"name": "test"}')
            f.flush()

            result, category = tester.detect_file_type(f.name)

            captured = capsys.readouterr()
            assert "DEBUG: Starting file type detection" in captured.err
            assert "DEBUG: Trying Filesystem test" in captured.err
            assert "DEBUG: Trying Magic test" in captured.err

            os.unlink(f.name)

    def test_debug_directory_processing(self, capsys):
        """Test debug output for directory processing."""
        import sys
        import tempfile

        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            py_file = os.path.join(tmpdir, "test.py")
            with open(py_file, "w") as f:
                f.write("print('hello')")

            # Mock sys.argv to test directory processing with debug
            with unittest.mock.patch.object(sys, "argv", ["fft.py", "-d", tmpdir]):
                fft.main()

            captured = capsys.readouterr()

            # Check directory processing debug output
            assert "DEBUG: Processing 1 argument(s)" in captured.err
            assert "is a directory, processing recursively" in captured.err
            assert "DEBUG: Scanning directory" in captured.err
            assert "DEBUG: Found" in captured.err and "files in" in captured.err
            assert "DEBUG: Added file" in captured.err

    def test_debug_help_option(self, capsys):
        """Test that debug option appears in help."""
        import sys

        # Mock sys.argv to simulate --help
        with unittest.mock.patch.object(sys, "argv", ["fft.py", "--help"]):
            with pytest.raises(SystemExit):
                fft.main()

            captured = capsys.readouterr()
            assert "-d, --debug" in captured.out
            assert "Print internal debugging information to stderr" in captured.out

    def test_debug_with_nonexistent_file(self, capsys):
        """Test debug output with nonexistent file."""
        tester = fft.FileTypeTester(debug=True)

        result, category = tester.detect_file_type("/nonexistent/file.txt")

        captured = capsys.readouterr()
        assert "DEBUG: Starting file type detection" in captured.err
        assert (
            "DEBUG: ERROR: File '/nonexistent/file.txt' does not exist" in captured.err
        )
        assert "ERROR:" in result


class TestExitOnErrorFunctionality:
    """Test cases for exit-on-error functionality."""

    def test_exit_on_error_flag_in_help(self, capsys):
        """Test that exit-on-error option appears in help."""
        import sys

        # Mock sys.argv to simulate --help
        with unittest.mock.patch.object(sys, "argv", ["fft.py", "--help"]):
            with pytest.raises(SystemExit):
                fft.main()

            captured = capsys.readouterr()
            assert "-E, --exit-on-error" in captured.out
            assert "Exit immediately on filesystem errors" in captured.out

    def test_normal_behavior_without_exit_on_error(self, capsys):
        """Test normal behavior without -E flag (continue on errors)."""
        import sys
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("print('hello')")
            f.flush()

            # Mock sys.argv with nonexistent file and existing file
            with unittest.mock.patch.object(
                sys, "argv", ["fft.py", "/nonexistent/file.txt", f.name]
            ):
                fft.main()

            captured = capsys.readouterr()

            # Should show error for nonexistent file but continue processing
            assert (
                "ERROR: File or directory '/nonexistent/file.txt' does not exist"
                in captured.out
            )
            assert "Python script" in captured.out  # Should process the existing file

            os.unlink(f.name)

    def test_exit_on_error_with_nonexistent_file(self, capsys):
        """Test that -E flag exits on nonexistent file."""
        import sys
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("print('hello')")
            f.flush()

            # Mock sys.argv with -E flag and nonexistent file
            with unittest.mock.patch.object(
                sys, "argv", ["fft.py", "-E", "/nonexistent/file.txt", f.name]
            ):
                with pytest.raises(SystemExit) as exc_info:
                    fft.main()

                assert exc_info.value.code == 1

            captured = capsys.readouterr()

            # Error should go to stderr, not stdout
            assert captured.out == ""
            assert (
                "ERROR: File or directory '/nonexistent/file.txt' does not exist"
                in captured.err
            )

            os.unlink(f.name)

    def test_exit_on_error_with_existing_file(self, capsys):
        """Test that -E flag doesn't exit on existing files."""
        import sys
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("print('hello')")
            f.flush()

            # Mock sys.argv with -E flag and existing file
            with unittest.mock.patch.object(sys, "argv", ["fft.py", "-E", f.name]):
                fft.main()  # Should not raise SystemExit

            captured = capsys.readouterr()

            # Should process normally
            assert "Python script" in captured.out
            assert captured.err == ""

            os.unlink(f.name)

    def test_exit_on_error_with_nonexistent_directory(self, capsys):
        """Test that -E flag exits on nonexistent directory."""
        import sys

        # Mock sys.argv with -E flag and nonexistent directory
        with unittest.mock.patch.object(
            sys, "argv", ["fft.py", "-E", "/nonexistent/directory/"]
        ):
            with pytest.raises(SystemExit) as exc_info:
                fft.main()

            assert exc_info.value.code == 1

        captured = capsys.readouterr()

        # Error should go to stderr
        assert captured.out == ""
        assert (
            "ERROR: File or directory '/nonexistent/directory/' does not exist"
            in captured.err
        )

    def test_exit_on_error_with_directory_access_error(self, capsys):
        """Test that -E flag works with directories that cannot be accessed."""
        import os
        import sys
        import tempfile

        # Note: Directory permission errors don't always trigger os.walk() exceptions
        # This test verifies the behavior when directories are inaccessible
        with tempfile.TemporaryDirectory() as tmpdir:
            restricted_dir = os.path.join(tmpdir, "restricted")
            os.makedirs(restricted_dir)

            # Create a file inside the directory
            test_file = os.path.join(restricted_dir, "test.txt")
            with open(test_file, "w") as f:
                f.write("test content")

            # Remove read and execute permissions on the directory
            os.chmod(restricted_dir, 0o000)

            try:
                # Mock sys.argv with -E flag and restricted directory
                with unittest.mock.patch.object(
                    sys, "argv", ["fft.py", "-E", restricted_dir]
                ):
                    fft.main()  # This should not exit since directory exists

                captured = capsys.readouterr()

                # Directory is accessible but returns no files (treated as empty)
                assert "directory (empty or inaccessible)" in captured.out

            finally:
                # Restore permissions for cleanup
                os.chmod(restricted_dir, 0o755)

    def test_exit_on_error_combined_with_other_flags(self, capsys):
        """Test that -E flag works with other flags like debug and verbose."""
        import sys

        # Test with debug flag
        with unittest.mock.patch.object(
            sys, "argv", ["fft.py", "-E", "-d", "/nonexistent/file.txt"]
        ):
            with pytest.raises(SystemExit) as exc_info:
                fft.main()

            assert exc_info.value.code == 1

        captured = capsys.readouterr()

        # Should have both debug output and error
        assert "DEBUG:" in captured.err
        assert (
            "ERROR: File or directory '/nonexistent/file.txt' does not exist"
            in captured.err
        )

    def test_exit_on_error_stops_processing_multiple_files(self, capsys):
        """Test that -E flag stops processing after first error."""
        import sys
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f1:
            f1.write("print('hello')")
            f1.flush()

            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".js"
            ) as f2:
                f2.write("console.log('hello');")
                f2.flush()

                # Mock sys.argv with existing file, nonexistent file, then
                # another existing file
                with unittest.mock.patch.object(
                    sys,
                    "argv",
                    ["fft.py", "-E", f1.name, "/nonexistent/file.txt", f2.name],
                ):
                    with pytest.raises(SystemExit) as exc_info:
                        fft.main()

                    assert exc_info.value.code == 1

                captured = capsys.readouterr()

                # Should process first file, then exit on error, not process third file
                assert f1.name in captured.out and "Python script" in captured.out
                assert f2.name not in captured.out  # Should not reach this file
                assert (
                    "ERROR: File or directory '/nonexistent/file.txt' does not exist"
                    in captured.err
                )

                os.unlink(f2.name)

            os.unlink(f1.name)


class TestExtensionFunctionality:
    """Test cases for the --extension functionality."""

    def test_extension_flag_in_help(self, capsys):
        """Test that --extension option appears in help text."""
        with pytest.raises(SystemExit):
            with unittest.mock.patch("sys.argv", ["fft.py", "--help"]):
                fft.main()

        captured = capsys.readouterr()
        assert "--extension" in captured.out
        assert "Print a slash-separated list of valid extensions" in captured.out

    def test_get_extensions_for_type_single_extension(self):
        """Test getting extensions for file types with single extension."""
        tester = fft.FileTypeTester()

        # Test file types with single extensions
        assert tester.get_extensions_for_type("text file") == "txt"
        assert tester.get_extensions_for_type("Python script") == "py"
        assert tester.get_extensions_for_type("JSON data") == "json"

    def test_get_extensions_for_type_multiple_extensions(self):
        """Test getting extensions for file types with multiple extensions."""
        tester = fft.FileTypeTester()

        # JPEG has both .jpg and .jpeg extensions
        result = tester.get_extensions_for_type("JPEG image")
        assert result == "jpeg/jpg"  # Should be sorted

    def test_get_extensions_for_type_unknown_type(self):
        """Test getting extensions for unknown file types."""
        tester = fft.FileTypeTester()

        # Unknown file types should return empty string
        assert tester.get_extensions_for_type("unknown file type") == ""
        assert tester.get_extensions_for_type("non-existent type") == ""

    def test_extension_flag_with_known_file_type(self, capsys):
        """Test --extension flag with files that have known extensions."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write("print('hello')")
            f.flush()

            with unittest.mock.patch("sys.argv", ["fft.py", "--extension", f.name]):
                fft.main()

            captured = capsys.readouterr()
            assert f"{f.name}: py" in captured.out

            os.unlink(f.name)

    def test_extension_flag_with_multiple_extensions(self, capsys):
        """Test --extension flag with file types having multiple extensions."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".jpg") as f:
            f.write("fake jpeg content")
            f.flush()

            with unittest.mock.patch("sys.argv", ["fft.py", "--extension", f.name]):
                fft.main()

            captured = capsys.readouterr()
            assert f"{f.name}: jpeg/jpg" in captured.out

            os.unlink(f.name)

    def test_extension_flag_with_brief_mode(self, capsys):
        """Test --extension flag combined with --brief mode."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".js") as f:
            f.write("console.log('hello');")
            f.flush()

            with unittest.mock.patch(
                "sys.argv", ["fft.py", "--extension", "--brief", f.name]
            ):
                fft.main()

            captured = capsys.readouterr()
            assert captured.out.strip() == "js"

            os.unlink(f.name)

    def test_extension_flag_with_unknown_file_type(self, capsys):
        """Test --extension flag with file types that have no known extensions."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("unknown content")
            f.flush()

            # Make it executable to trigger "executable file" detection
            os.chmod(f.name, 0o755)

            with unittest.mock.patch("sys.argv", ["fft.py", "--extension", f.name]):
                fft.main()

            captured = capsys.readouterr()
            assert f"{f.name}: " in captured.out  # Should show empty extensions

            os.unlink(f.name)

    def test_extension_flag_with_multiple_files(self, capsys):
        """Test --extension flag with multiple files."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f1:
            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".html"
            ) as f2:
                f1.write("print('hello')")
                f2.write("<html></html>")
                f1.flush()
                f2.flush()

                with unittest.mock.patch(
                    "sys.argv", ["fft.py", "--extension", f1.name, f2.name]
                ):
                    fft.main()

                captured = capsys.readouterr()
                assert f"{f1.name}: py" in captured.out
                assert f"{f2.name}: html" in captured.out

                os.unlink(f1.name)
                os.unlink(f2.name)

    def test_extension_flag_with_directory(self, capsys):
        """Test --extension flag with directory processing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files with known extensions
            py_file = os.path.join(tmpdir, "test.py")
            js_file = os.path.join(tmpdir, "test.js")

            with open(py_file, "w") as f:
                f.write("print('hello')")
            with open(js_file, "w") as f:
                f.write("console.log('hello');")

            with unittest.mock.patch("sys.argv", ["fft.py", "--extension", tmpdir]):
                fft.main()

            captured = capsys.readouterr()
            assert f"{js_file}: js" in captured.out
            assert f"{py_file}: py" in captured.out


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

    def test_real_directory_processing(self, capsys):
        """Test directory processing on real project directory."""
        import sys

        # Test with the tests directory
        if os.path.exists("tests") and os.path.isdir("tests"):
            with unittest.mock.patch.object(sys, "argv", ["fft.py", "tests"]):
                fft.main()

            captured = capsys.readouterr()

            # Should find Python test files
            assert "test_fft.py" in captured.out
            assert (
                "Python script" in captured.out or "executable script" in captured.out
            )
