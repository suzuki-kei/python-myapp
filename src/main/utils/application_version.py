"""
    アプリケーションのバージョンを扱う機能を提供する.

    バージョンの形式
    ----------------
    アプリケーションのバージョンは以下のいずれかの形式で表現する.

        * <major>.<minor>.<patch> (Ex. "1.2.3")
        * <major>.<minor>.<patch>-<suffix> (Ex. "1.2.3-SNAPSHOT")

    Frequently Variable Names
    -------------------------
    version : ApplicationVersion
        アプリケーションのバージョン.

    version_string : str
        バージョンの文字列表現.
        例えば "1.2.3" や "1.2.3-SNAPSHOT" が有効な値.

    version_components : tuple(int, int, int, str|None)
        バージョンの構成要素からなる tuple.

    major_version : int
        メジャーバージョン.

    minor_version : int
        マイナーバージョン.

    patch_version : int
        パッチバージョン.

    version_suffix : str|None
        サフィックス.

    Examples
    --------

        # インスタンスを生成する.
        version = ApplicationVersion(1, 2, 3)
        print(version) # => "1.2.3"

        # バージョン文字列からインスタンスを生成する.
        version = from_string("1.2.3")
        print(version) # => "1.2.3"

        # バージョン文字列が保存されたファイルからインスタンスを生成する.
        version_file_path = ...
        version = from_file(version_file_path)
        print(version) # => "1.2.3"

        # バージョンを変更する.
        version = from_string("1.2.3-SNAPSHOT")
        print(version)                   # => "1.2.3-SNAPSHOT"
        print(version.bump_major())      # => "2.0.0-SNAPSHOT"
        print(version.bump_minor())      # => "1.3.0-SNAPSHOT"
        print(version.bump_patch())      # => "1.2.4-SNAPSHOT"
        print(version.bump_to_release()) # => "1.2.3"
"""

import re
import typing
import utils.comparable


VERSION_STRING_PATTERN = re.compile(
    r"\A(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-([a-zA-Z0-9]+))?\Z",
    re.MULTILINE)
"""バージョン文字列にマッチする正規表現."""


class InvalidVersion(ValueError):
    """
        無効なバージョンであることを表す例外.
    """


@utils.comparable.comparable
class ApplicationVersion(object):
    """
        アプリケーションのバージョン.
    """

    __slots__ = ("_major", "_minor", "_patch", "_suffix")

    def __init__(
            self: "ApplicationVersion",
            major: int,
            minor: int,
            patch: int,
            suffix: typing.Optional[str]=None
            ) -> None:
        """
            インスタンスを初期化する.

            Arguments
            ---------
            major : int
                メジャーバージョン.
            minor : int
                マイナーバージョン.
            patch : int
                パッチバージョン.
            suffix : str|None
                サフィックス.

            Raises
            ------
            InvalidVersion
                引数から有効なバージョンを構成できない場合.
        """
        # 無効なバージョンの場合は InvalidVersion が発生する.
        build_version_string(major, minor, patch, suffix)

        self._major = major
        self._minor = minor
        self._patch = patch
        self._suffix = suffix

    def __str__(self: "ApplicationVersion") -> str:
        """
            バージョンの文字列表現を返す.

            Returns
            -------
            version_string : str
                バージョンの文字列表現.
        """
        return build_version_string(*self.components)

    @property
    def components(
            self: "ApplicationVersion"
            ) -> typing.Tuple[int, int, int, typing.Optional[str]]:
        """
            バージョンの構成要素からなる tuple.

            Returns
            -------
            components : tuple(int, int, int, str|None)
                バージョンの構成要素からなる tuple.
        """
        return (self._major, self._minor, self._patch, self._suffix)

    @property
    def major(self: "ApplicationVersion") -> int:
        """
            メジャーバージョン.

            Returns
            -------
            major : int
                メジャーバージョン.
        """
        return self._major

    @property
    def minor(self: "ApplicationVersion") -> int:
        """
            マイナーバージョン.

            Returns
            -------
            minor : int
                マイナーバージョン.
        """
        return self._minor

    @property
    def patch(self: "ApplicationVersion") -> int:
        """
            パッチバージョン.

            Returns
            -------
            patch : int
                パッチバージョン.
        """
        return self._patch

    @property
    def suffix(self: "ApplicationVersion") -> typing.Optional[str]:
        """
            サフィックス.

            Returns
            -------
            suffix : str|None
                サフィックス.
        """
        return self._suffix

    def compare(self: "ApplicationVersion", other: "ApplicationVersion") -> int:
        """
            他のインスタンスと順序を比較する.

            Arguments
            ---------
            other : ApplicationVersion
                比較対象のインスタンス.

            Returns
            -------
            int
                other より小さい場合は負数.
                other と等しい場合は 0.
                other より大きい場合は正数.
        """
        self_compare_key = to_compare_key(self)
        other_compare_key = to_compare_key(other)
        if self_compare_key < other_compare_key:
            return -1
        if self_compare_key > other_compare_key:
            return +1
        return 0

    def bump_major(self: "ApplicationVersion") -> "ApplicationVersion":
        """
            メジャーバージョンを上げる.

            Returns
            -------
            ApplicationVersion
                新しいバージョンを表すインスタンス.
        """
        return self.__class__(self._major + 1, 0, 0, self._suffix)

    def bump_minor(self: "ApplicationVersion") -> "ApplicationVersion":
        """
            マイナーバージョンを上げる.

            Returns
            -------
            ApplicationVersion
                新しいバージョンを表すインスタンス.
        """
        return self.__class__(self._major, self._minor + 1, 0, self._suffix)

    def bump_patch(self: "ApplicationVersion") -> "ApplicationVersion":
        """
            パッチバージョンを上げる.

            Returns
            -------
            ApplicationVersion
                新しいバージョンを表すインスタンス.
        """
        return self.__class__(self._major, self._minor, self._patch + 1, self._suffix)

    def bump_suffix(
            self: "ApplicationVersion",
            suffix: typing.Optional[str]
            ) -> "ApplicationVersion":
        """
            バージョンサフィックスを変更する.

            Returns
            -------
            ApplicationVersion
                新しいバージョンを表すインスタンス.
        """
        return self.__class__(self._major, self._minor, self._patch, suffix)

    def bump_to_release(
            self: "ApplicationVersion"
            ) -> "ApplicationVersion":
        """
            リリースバージョンに変更する.

            Returns
            -------
            ApplicationVersion
                新しいバージョンを表すインスタンス.
        """
        return self.bump_suffix(None)

    def bump_to_snapshot(
            self: "ApplicationVersion"
            ) -> "ApplicationVersion":
        """
            スナップショットバージョンに変更する.

            Returns
            -------
            ApplicationVersion
                新しいバージョンを表すインスタンス.
        """
        return self.bump_suffix("SNAPSHOT")

    def save(
            self: "ApplicationVersion",
            file_path: str
            ) -> None:
        """
            ファイルに保存する.

            Arguments
            ---------
            file_path : str
                保存先ファイルのパス.
        """
        with open(file_path, "w") as file:
            file.write(str(self))


def from_file(file_path: str) -> None:
    """
        バージョン文字列が保存されたファイルから ApplicationVersion を生成する.

        Arguments
        ---------
        file_path : str
            バージョン文字列が保存されたファイルのパス.

        Returns
        -------
        ApplicationVersion
            ファイルで指定されたバージョンを表す ApplicationVersion.
    """
    with open(file_path, "r") as file:
        version_string = file.read().strip()
        return from_string(version_string)


def from_string(version_string: str) -> "ApplicationVersion":
    """
        バージョン文字列から ApplicationVersion を生成する.

        Arguments
        ---------
        version_string : str
            バージョン文字列.
            Ex. "1.2.3-SNAPSHOT".

        Returns
        -------
        ApplicationVersion
            文字列で指定されたバージョンを表す ApplicationVersion.
    """
    versions = parse_version_string(version_string)
    return ApplicationVersion(*versions)


def parse_version_string(
        version_string: str
        ) -> typing.Tuple[int, int, int, typing.Optional[str]]:
    """
        バージョン文字列をパースする.

        Arguments
        ---------
        version_string : str
            バージョン文字列.
            Ex. "1.2.3-SNAPSHOT".

        Returns
        -------
        tuple(int, int, int, str|None)
            以下を含む tuple.
             * メジャーバージョン
             * マイナーバージョン
             * パッチバージョン
             * サフィックス

        Raises
        ------
        InvalidVersion
            version_string が有効な形式ではない場合.
    """
    matched = VERSION_STRING_PATTERN.match(version_string)
    if not matched:
        raise InvalidVersion(version_string)
    return (int(matched[1]), int(matched[2]), int(matched[3]), matched[4])


def build_version_string(
        major: int,
        minor: int,
        patch: int,
        suffix: typing.Optional[str]=None
        ) -> str:
    """
        バージョン文字列を構築する.

        Arguments
        ---------
        major : int
            メジャーバージョン.
        minor : int
            マイナーバージョン.
        patch : int
            パッチバージョン.
        suffix : str|None
            バージョンサフィックス.

        Returns
        -------
        str
            引数から構築したバージョン文字列.
    """
    if suffix is None:
        version_string = "{}.{}.{}".format(major, minor, patch)
    else:
        version_string = "{}.{}.{}-{}".format(major, minor, patch, suffix)

    if not VERSION_STRING_PATTERN.match(version_string):
        raise InvalidVersion(version_string)

    return version_string


def to_compare_key(
        version: "ApplicationVersion"
        ) -> typing.Tuple[int, int, int, bool, str]:
    """
        比較用のキーに変換する.

        Arguments
        ---------
        version : ApplicationVersion
            ApplicationVersion.

        Returns
        -------
        tuple(int, int, int, bool, str)
            比較用のキー.
    """
    major, minor, patch, suffix = version.components
    return (major, minor, patch, suffix is None, str(suffix))

