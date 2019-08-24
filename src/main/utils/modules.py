import os
import re
from functools import partial
from importlib import import_module

from utils.files import generate_file_paths

MODULE_FILE_PATH_PATTERN = re.compile(r"^([^/]+/)*[a-zA-Z0-9][a-zA-Z0-9_]*\.py$")

def find_modules(scan_dir):
    file_paths = generate_file_paths(scan_dir)

    to_relative_path = partial(os.path.relpath, start=scan_dir)
    file_paths = map(to_relative_path, file_paths)

    is_module_file_path = MODULE_FILE_PATH_PATTERN.match
    file_paths = filter(is_module_file_path, file_paths)

    to_module_name = lambda file_path: file_path.rstrip(".py").replace("/", ".")
    module_names = map(to_module_name, file_paths)

    return module_names

def import_modules(scan_dir):
    return list(map(import_module, find_modules(scan_dir)))

