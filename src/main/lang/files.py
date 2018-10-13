import os

def generate_paths(scan_dir):
    for dirpath, dirnames, filenames in os.walk(scan_dir):
        for dirname in dirnames:
            yield os.path.join(dirpath, dirname)
        for filename in filenames:
            yield os.path.join(dirpath, filename)

def generate_file_paths(scan_dir):
    for dirpath, dirnames, filenames in os.walk(scan_dir):
        for filename in filenames:
            yield os.path.join(dirpath, filename)

def generate_directory_paths(scan_dir):
    for dirpath, dirnames, filenames in os.walk(scan_dir):
        for dirname in dirnames:
            yield os.path.join(dirpath, dirname)

