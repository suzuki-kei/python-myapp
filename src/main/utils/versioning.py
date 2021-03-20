"""
    Provides functionality of versioning.

    Frequently Used Names and Variables
    -----------------------------------
    version : Version
        A instance of Version class.

    version_string : str
        A version by string representation.
        Ex. '1.2.3-SNAPSHOT'.

    major : int
        A major version.
        Ex. 1.

    minor : int
        A minor version.
        Ex. 2.

    patch : int
        A patch version.
        Ex. 3.

    suffix : str|None
        A suffix of version.
        Ex. 'SNAPSHOT'.
"""


import re
import typing


VERSION_STRING_PATTERN: re.Pattern = re.compile(
    r'\A(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-([a-zA-Z0-9]+))?\Z',
    re.MULTILINE)
"""
    re.Patern
        A regular expression that matches version string.
"""


def from_file(
        file_path: str
        ) -> 'Version':
    """
        Create new Version from version file.

        Arguments
        ---------
        file_path : str
            A file path that contains version string.

        Returns
        -------
        version : Version
            New Version instance.

        Raises
        ------
        InvalidVersion
            A file contains invalid version string.
    """
    with open(file_path) as file:
        version_string = file.read().strip()
        return from_string(version_string)


def from_string(
        version_string: str
        ) -> 'Version':
    """
        Create new Version from version string.

        Arguments
        ---------
        version_string : str
            A version string.

        Returns
        -------
        version : Version
            New Version instance.

        Raises
        ------
        InvalidVersion
            Raises when version_string is invalid.
    """
    major, minor, patch, suffix = parse_version(version_string)
    return Version(major, minor, patch, suffix)


def parse_version_string(
        version_string: str
        ) -> typing.Tuple[int, int, int, typing.Optional[str]]:
    """
        Parse version string.

        Arguments
        ---------
        version_string : str
            Version string.

        Returns
        -------
        major, minor, patch, suffix : tuple(int, int, int, str|None)
            Elements of version string.

        Raises
        ------
        InvalidVersion
            Raises when invalid version string.
    """
    matched = VERSION_STRING_PATTERN.match(version_string)
    if matched:
        return (int(matched[1]), int(matched[2]), int(matched[3]), matched[4])
    else:
        raise InvalidVersion(version_string)


def build_version_string(
        major: int,
        minor: int,
        patch: int,
        suffix: typing.Optional[str]
        ) -> str:
    """
        Build version string.

        Arguments
        ---------
        major : int
            A major version.

        minor : int
            A minor version.

        patch : int
            A patch version.

        suffix : str|None
            A suffix of version.

        Returns
        -------
        version_string : str
            A version string.
    """
    if suffix is None:
        version_string = '{}.{}.{}'.format(major, minor, patch)
    else:
        version_string = '{}.{}.{}-{}'.format(major, minor, patch, suffix)

    parse_version_string(version_string)

    return version_string


class InvalidVersion(ValueError):
    """
        Raises when version is invalid.
    """


class Version(object):
    """
        Version.

        Traits
        ------
         * This class is immutable.
         * This class is thread safe.

        Properties
        ----------
        TODO
    """

    __slots__ = (
            '_major',
            '_minor',
            '_patch',
            '_suffix',
    )

    def __init__(
            self: 'Version',
            major: int,
            minor: int,
            patch: int,
            suffix: typing.Optional[str]=None
            ) -> None:
        """
            Initialize instance by arguments.

            Arguments
            ---------
            major : int
                A major version.
            minor : int
                A minor version.
            patch : int
                A patch version.
            suffix : str|None
                A suffix of version.
        """
        self._major = major
        self._minor = minor
        self._patch = patch
        self._suffix = suffix

    @property
    def major(self):
        """
            Major version.

            Returns
            -------
            major : int
                Major version.
        """
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def patch(self):
        return self._patch

    @property
    def suffix(self):
        return self._suffix

    def __str__(self):
        return build_version_string(
                self._major,
                self._minor,
                self._patch,
                self._suffix)

    def bump_major(
            self: 'Version'
            ) -> 'Version':
        return Version(self._major + 1, 0, 0, self._suffix)

    def bump_minor(
            self: 'Version'
            ) -> 'Version':
        return Version(self._major, self._minor + 1, 0, self._suffix)

    def bump_patch(
            self: 'Version'
            ) -> 'Version':
        return Version(self._major, self._minor, self._patch + 1, self._suffix)

    def bump_suffix(
            self: 'Version',
            suffix: str
            ) -> 'Version':
        return Version(self._major, self._minor, self._patch, suffix)

    def bump_to_release(
            self: 'Version'
            ) -> 'Version':
        return self.bump_to_suffix(None)

    def bump_to_snapshot(
            self: 'Version'
            ) -> 'Version':
        return self.bump_to_suffix('SNAPSHOT')

    def save(
            self: 'Version',
            file_path: str
            ) -> None:
        with open(file_path, 'w') as file:
            file.write(str(self))

