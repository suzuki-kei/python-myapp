import re
from utils.comparable import comparable

@comparable
class ApplicationVersion(object):
    """
        アプリケーションのバージョン.

        バージョンは以下のいずれかの形式であることを前提とする.

            * <major>.<minor>.<patch> (Ex. "1.2.3")
            * <major>.<minor>.<patch>-<suffix> (Ex. "1.2.3-SNAPSHOT")

        Examples
        --------

            # インスタンスの生成.
            version = ApplicationVersion(1, 2, 3)
            print(version) # => "1.2.3"

            # バージョン文字列からインスタンを生成する.
            version = ApplicationVersion.from_version_string("1.2.3")
            print(version) # => "1.2.3"

            # バージョン文字列が保存されたファイルからインスタンスを生成する.
            version_file_path = ...
            version = ApplicationVersion.from_file(version_file_path)
            print(version) # => "1.2.3"

            # バージョンを変更する.
            version = ApplicationVersion.from_version_string("1.2.3-SNAPSHOT")
            print(version)                 # => "1.2.3-SNAPSHOT"
            print(version.bump_major)      # => "2.0.0-SNAPSHOT"
            print(version.bump_minor)      # => "1.3.0-SNAPSHOT"
            print(version.bump_patch)      # => "1.2.4-SNAPSHOT"
            print(version.bump_to_release) # => "1.2.3"
    """

    # バージョン文字列にマッチする正規表現.
    VERSION_STRING_PATTERN = re.compile(r"\A(\d+)\.(\d+)\.(\d)+(?:-(.+))?\Z", re.MULTILINE)

    @classmethod
    def from_file(self, file_path):
        """
            バージョン文字列が保存されたファイルからインスタンスを生成する.

            Arguments
            ---------
            file_path : str
                バージョン文字列が保存されたファイルのパス.

            Returns
            -------
            ApplicationVersion
                新しく生成したインスタンス.
        """
        with open(file_path, "r") as file:
            version_string = file.read().strip()
            return self.from_version_string(version_string)

    @classmethod
    def from_version_string(self, version_string):
        """
            バージョン文字列からインスタンスを生成する.

            Arguments
            ---------
            version_string : str
                バージョン文字列.
                Ex. "1.2.3-SNAPSHOT".

            Returns
            -------
            ApplicationVersion
                新しく生成したインスタンス.
        """
        versions = self._parse_version_string(version_string)
        return self(*versions)

    @classmethod
    def _parse_version_string(self, version_string):
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
                メジャーバージョン, マイナーバージョン,
                パッチバージョン, サフィックスを含む tuple.
        """
        matched = self.VERSION_STRING_PATTERN.match(version_string)
        if not matched:
            raise ValueError("Invalid version string", version_string)

        return (int(matched[1]), int(matched[2]), int(matched[3]), matched[4])

    @classmethod
    def _build_version_string(self, major, minor, patch, suffix):
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

            Returns:
                str: 引数から構築したバージョン文字列.
        """
        if suffix:
            return "{}.{}.{}-{}".format(major, minor, patch, suffix)
        else:
            return "{}.{}.{}".format(major, minor, patch)

    def __init__(self, major, minor, patch, suffix=None):
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
                バージョンサフィックス.

            Returns
            -------
            ApplicationVersion
                初期化済みインスタンス.
        """
        self._major = major
        self._minor = minor
        self._patch = patch
        self._suffix = suffix

    def __repr__(self):
        return self.__class__._build_version_string(self._major, self._minor, self._patch, self._suffix)

    def compare(self, other):
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
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self._major < other._major:
            return -1
        if self._major > other._major:
            return +1
        if self._minor < other._minor:
            return -1
        if self._minor > other._minor:
            return +1
        if self._patch < other._patch:
            return -1
        if self._patch > other._patch:
            return +1
        if self._suffix == None and other._suffix == None:
            return 0
        if self._suffix != None and other._suffix == None:
            return -1
        if self._suffix == None and other._suffix != None:
            return +1
        if self._suffix < other._suffix:
            return -1
        if self._suffix > other._suffix:
            return +1
        return 0

    @property
    def major(self):
        """
            メジャーバージョンを返す.

            Returns
            -------
            int
                メジャーバージョン.
        """
        return self._major

    @property
    def minor(self):
        """
            マイナーバージョンを返す.

            Returns
            -------
            int
                マイナーバージョン.
        """
        return self._minor

    @property
    def patch(self):
        """
            パッチバージョンを返す.

            Returns
            -------
            int
                パッチバージョン.
        """
        return self._patch

    @property
    def suffix(self):
        """
            バージョンサフィックスを返す.

            Returns
            -------
            str
                バージョンサフィックス.
        """
        return self._suffix

    def bump_major(self):
        """
            メジャーバージョンを上げる.

            Returns
            -------
            ApplicationVersion
                新しいバージョンを表すインスタンス.
        """
        return self.__class__(self._major + 1, 0, 0, self._suffix)

    def bump_minor(self):
        """
            マイナーバージョンを上げる.

            Returns
            -------
            ApplicationVersion
                新しいバージョンを表すインスタンス.
        """
        return self.__class__(self._major, self._minor + 1, 0, self._suffix)

    def bump_patch(self):
        """
            パッチバージョンを上げる.

            Returns
            -------
            ApplicationVersion
                新しいバージョンを表すインスタンス.
        """
        return self.__class__(self._major, self._minor, self._patch + 1, self._suffix)

    def bump_suffix(self, suffix):
        """
            バージョンサフィックスを変更する.

            Returns
            -------
            ApplicationVersion
                新しいバージョンを表すインスタンス.
        """
        return self.__class__(self._major, self._minor, self._patch, suffix)

    def bump_to_release(self):
        """
            リリースバージョンに変更する.

            Returns
            -------
            ApplicationVersion
                新しいバージョンを表すインスタンス.
        """
        return self.bump_suffix(None)

    def bump_to_snapshot(self):
        """
            スナップショットバージョンに変更する.

            Returns
            -------
            ApplicationVersion
                新しいバージョンを表すインスタンス.
        """
        return self.bump_suffix("SNAPSHOT")

    def save(self, file_path):
        """
            ファイルに保存する.

            Arguments
            ---------
            file_path : str
                保存先ファイルのパス.
        """
        with open(file_path, "w") as file:
            file.write(str(self))

