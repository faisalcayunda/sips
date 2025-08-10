#!/usr/bin/env python3
"""
Test runner script for SIPS project.
"""

import os
import subprocess
import sys


def run_tests():
    """Run all tests with pytest."""
    # Get the directory where this script is located
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(test_dir)

    # Change to project root directory
    os.chdir(project_root)

    # Run pytest with appropriate options
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--strict-markers",  # Strict marker checking
        "--disable-warnings",  # Disable warnings
        "--color=yes",  # Colored output
    ]

    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed successfully!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode


def run_specific_test(test_path):
    """Run a specific test file or test function."""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(test_dir)

    os.chdir(project_root)

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        test_path,
        "-v",
        "--tb=short",
        "--color=yes",
    ]

    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✅ Test {test_path} passed successfully!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Test {test_path} failed with exit code {e.returncode}")
        return e.returncode


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_path = sys.argv[1]
        exit_code = run_specific_test(test_path)
    else:
        # Run all tests
        exit_code = run_tests()

    sys.exit(exit_code)
