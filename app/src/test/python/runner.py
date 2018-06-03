from os import path
from unittest import TestLoader
from unittest import TextTestRunner

def _discover_tests():
    root_dir = path.abspath(path.join(path.dirname(__file__), "..", "..", ".."))
    start_dir = path.abspath(path.join(path.dirname(__file__)))
    file_pattern = "test_*.py"
    return TestLoader().discover(start_dir, file_pattern, root_dir)

def _run_tests():
    test_suite = _discover_tests()
    TextTestRunner().run(test_suite)

if __name__ == "__main__":
    _run_tests()

