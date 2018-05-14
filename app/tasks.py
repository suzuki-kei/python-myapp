import sys
from glob import glob
from importlib import import_module
from os import path

import invoke

def import_modules(directory_path):
    if directory_path not in sys.path:
        sys.path.append(directory_path)

    file_paths = glob(path.join(directory_path, "[a-zA-Z0-9]*.py"))
    file_names = map(path.basename, file_paths)
    module_names = [path.splitext(file_name)[0] for file_name in file_names]
    return map(import_module, module_names)

namespace = invoke.Collection(*import_modules(path.join(path.dirname(__file__), "tasks")))

