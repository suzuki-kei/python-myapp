import os
import functools


def generate_paths(root_path):
    """
        ファイル/ディレクトリのパスを生成する.

        Arguments
        ---------
        root_path : str
            スキャンを開始するディレクトリのパス.

        Yields
        ------
        path : str
            ファイルまたはディレクトリのパス.
    """
    yield from _generate_paths(
        root_path,
        include_files=True,
        include_directories=True)


def generate_file_paths(root_path):
    """
        ファイルのパスを生成する.

        Arguments
        ---------
        root_path : str
            スキャンを開始するディレクトリのパス.

        Yields
        ------
        file_path : str
            ファイルのパス.
    """
    yield from _generate_paths(
        root_path,
        include_files=True,
        include_directories=False)


def generate_directory_paths(root_path):
    """
        ディレクトリのパスを生成する.

        Arguments
        ---------
        root_path : str
            スキャンを開始するディレクトリのパス.

        Yields
        ------
        directory_path : str
            ディレクトリのパス.
    """
    yield from _generate_paths(
        root_path,
        include_files=False,
        include_directories=True)


def _generate_paths(root_path, *, include_files=True, include_directories=True):
    """
        ファイルやディレクトリのパスを生成する.

        Arguments
        ---------
        root_path : str
            スキャンを開始するディレクトリのパス.
        include_files : bool
            結果にファイルのパスを含める場合は True を指定する.
        include_directories : bool
            結果にディレクトリのパスを含める場合は True を指定する.

        Yields
        ------
        path : str
            ファイルまたはディレクトリのパス.
    """
    for directory_path, directory_names, file_names in os.walk(root_path):
        join = functools.partial(os.path.join, directory_path)
        if include_files:
            yield from map(join, file_names)
        if include_directories:
            yield from map(join, directory_names)

