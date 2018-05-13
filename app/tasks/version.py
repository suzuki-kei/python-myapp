from invoke import task

from myapp.utilities.application_version import ApplicationVersion

VERSION_FILE_PATH = "./VERSION"

@task(default=True)
def show(context):
    """
        アプリケーションのバージョンを表示する.
    """
    version = ApplicationVersion.from_file(VERSION_FILE_PATH)
    print(version)

@task
def initialize(context, version):
    """
        アプリケーションのバージョンを初期化する.

        Args:
            version (str):
                バージョン文字列.
                Ex. "1.2.3-SNAPSHOT"
    """
    version = ApplicationVersion.from_version_string(version)
    version.save(VERSION_FILE_PATH)
    print("set version to {}".format(version))

@task
def bump_major(context):
    """
        アプリケーションのメジャーバージョンを上げる.
        例えば現在のバージョンが 1.2.3 の場合, 2.0.0 となる.
    """
    _bump_application_version(ApplicationVersion.bump_major)

@task
def bump_minor(context):
    """
        アプリケーションのマイナーバージョンを上げる.
        例えば現在のバージョンが 1.2.3 の場合, 1.3.0 となる.
    """
    _bump_application_version(ApplicationVersion.bump_minor)

@task
def bump_patch(context):
    """
        アプリケーションのパッチバージョンを上げる.
        例えば現在のバージョンが 1.2.3 の場合, 1.2.4 となる.
    """
    _bump_application_version(ApplicationVersion.bump_patch)

@task
def bump_to_release(context):
    """
        アプリケーションのバージョンをリリースバージョンに変更する.
        例えば現在のバージョンが 1.2.3-SNAPSHOT の場合, 1.2.3 となる.
    """
    _bump_application_version(ApplicationVersion.bump_to_release)

@task
def bump_to_snapshot(context):
    """
        アプリケーションのバージョンをスナップショットバージョンに変更する.
        例えば現在のバージョンが 1.2.3 の場合, 1.2.3-SNAPSHOT となる.
    """
    _bump_application_version(ApplicationVersion.bump_to_snapshot)

def _bump_application_version(bump_method):
    """
        アプリケーションのバージョンを変更する.

        Args:
            bump_method (instancemethod):
                バージョンを変更する ApplicationVersion のメソッド.
                Ex. ApplicationVersion.bump_major
    """
    old_version = ApplicationVersion.from_file(VERSION_FILE_PATH)
    new_version = bump_method(old_version)
    new_version.save(VERSION_FILE_PATH)
    print("bump version {} to {}".format(old_version, new_version))

