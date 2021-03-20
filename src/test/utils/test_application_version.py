from unittest import TestCase

from utils.application_version import ApplicationVersion
from utils.application_version import VERSION_STRING_PATTERN
from utils.application_version import InvalidVersion
from utils.application_version import from_file
from utils.application_version import from_string
from utils.application_version import parse_version_string
from utils.application_version import build_version_string
from utils.application_version import to_compare_key


class VersionStringPatternTestCase(TestCase):

    def test(self):
        # TODO
        VERSION_STRING_PATTERN.match("1.2.3")
        VERSION_STRING_PATTERN.match("1.2.3-SNAPSHOT")


class ApplicationVersionTestCase(TestCase):

    def test_constructor(self):
        self.assertEqual(
            "1.2.3",
            str(ApplicationVersion(1, 2, 3)))
        # TODO
        ##self.assertEqual(
        ##    "1.2.3",
        ##    str(ApplicationVersion(1, 2, 3, "")))
        self.assertEqual(
            "1.2.3",
            str(ApplicationVersion(1, 2, 3, None)))
        self.assertEqual(
            "1.2.3-SNAPSHOT",
            str(ApplicationVersion(1, 2, 3, "SNAPSHOT")))
        self.assertEqual(
            "1.2.3-Alpha",
            str(ApplicationVersion(1, 2, 3, "Alpha")))

    def test_properties(self):
        version = ApplicationVersion(1, 2, 3)
        self.assertEqual(1, version.major)
        self.assertEqual(2, version.minor)
        self.assertEqual(3, version.patch)
        self.assertEqual(None, version.suffix)

        version = ApplicationVersion(1, 2, 3, "SNAPSHOT")
        self.assertEqual(1, version.major)
        self.assertEqual(2, version.minor)
        self.assertEqual(3, version.patch)
        self.assertEqual("SNAPSHOT", version.suffix)

    def test_bump_major(self):
        version = ApplicationVersion(1, 2, 3)
        new_version = version.bump_major()
        self.assertEqual("1.2.3", str(version))
        self.assertEqual("2.0.0", str(new_version))

    def test_bump_minor(self):
        version = ApplicationVersion(1, 2, 3)
        new_version = version.bump_minor()
        self.assertEqual("1.2.3", str(version))
        self.assertEqual("1.3.0", str(new_version))

    def test_bump_patch(self):
        version = ApplicationVersion(1, 2, 3)
        new_version = version.bump_patch()
        self.assertEqual("1.2.3", str(version))
        self.assertEqual("1.2.4", str(new_version))

    def test_bump_suffix(self):
        version = ApplicationVersion(1, 2, 3)
        new_version = version.bump_suffix("Alpha")
        self.assertEqual("1.2.3", str(version))
        self.assertEqual("1.2.3-Alpha", str(new_version))

    def test_bump_to_snapshot(self):
        version = ApplicationVersion(1, 2, 3)
        new_version = version.bump_to_snapshot()
        self.assertEqual("1.2.3", str(version))
        self.assertEqual("1.2.3-SNAPSHOT", str(new_version))

    def test_bump_to_release(self):
        version = ApplicationVersion(1, 2, 3, "SNAPSHOT")
        new_version = version.bump_to_release()
        self.assertEqual("1.2.3-SNAPSHOT", str(version))
        self.assertEqual("1.2.3", str(new_version))

    def test_eq(self):
        self.assertEqual(True, ApplicationVersion(1, 2, 3) == ApplicationVersion(1, 2, 3))
        self.assertEqual(False, ApplicationVersion(1, 2, 3) == ApplicationVersion(1, 2, 4))
        self.assertEqual(False, ApplicationVersion(1, 2, 4) == ApplicationVersion(1, 2, 3))

        self.assertEqual(False, ApplicationVersion(1, 2, 3) == ApplicationVersion(1, 2, 3, "SNAPSHOT"))
        self.assertEqual(False, ApplicationVersion(1, 2, 3) == ApplicationVersion(1, 2, 4, "SNAPSHOT"))
        self.assertEqual(False, ApplicationVersion(1, 2, 4) == ApplicationVersion(1, 2, 3, "SNAPSHOT"))

        self.assertEqual(False, ApplicationVersion(1, 2, 3, "SNAPSHOT") == ApplicationVersion(1, 2, 3))
        self.assertEqual(False, ApplicationVersion(1, 2, 3, "SNAPSHOT") == ApplicationVersion(1, 2, 4))
        self.assertEqual(False, ApplicationVersion(1, 2, 4, "SNAPSHOT") == ApplicationVersion(1, 2, 3))

        self.assertEqual(True, ApplicationVersion(1, 2, 3, "SNAPSHOT") == ApplicationVersion(1, 2, 3, "SNAPSHOT"))
        self.assertEqual(False, ApplicationVersion(1, 2, 3, "SNAPSHOT") == ApplicationVersion(1, 2, 4, "SNAPSHOT"))
        self.assertEqual(False, ApplicationVersion(1, 2, 4, "SNAPSHOT") == ApplicationVersion(1, 2, 3, "SNAPSHOT"))

    def test_ne(self):
        self.assertEqual(False, ApplicationVersion(1, 2, 3) != ApplicationVersion(1, 2, 3))
        self.assertEqual(True, ApplicationVersion(1, 2, 3) != ApplicationVersion(1, 2, 4))
        self.assertEqual(True, ApplicationVersion(1, 2, 4) != ApplicationVersion(1, 2, 3))

        self.assertEqual(True, ApplicationVersion(1, 2, 3) != ApplicationVersion(1, 2, 3, "SNAPSHOT"))
        self.assertEqual(True, ApplicationVersion(1, 2, 3) != ApplicationVersion(1, 2, 4, "SNAPSHOT"))
        self.assertEqual(True, ApplicationVersion(1, 2, 4) != ApplicationVersion(1, 2, 3, "SNAPSHOT"))

        self.assertEqual(True, ApplicationVersion(1, 2, 3, "SNAPSHOT") != ApplicationVersion(1, 2, 3))
        self.assertEqual(True, ApplicationVersion(1, 2, 3, "SNAPSHOT") != ApplicationVersion(1, 2, 4))
        self.assertEqual(True, ApplicationVersion(1, 2, 4, "SNAPSHOT") != ApplicationVersion(1, 2, 3))

        self.assertEqual(False, ApplicationVersion(1, 2, 3, "SNAPSHOT") != ApplicationVersion(1, 2, 3, "SNAPSHOT"))
        self.assertEqual(True, ApplicationVersion(1, 2, 3, "SNAPSHOT") != ApplicationVersion(1, 2, 4, "SNAPSHOT"))
        self.assertEqual(True, ApplicationVersion(1, 2, 4, "SNAPSHOT") != ApplicationVersion(1, 2, 3, "SNAPSHOT"))

    def test_lt(self):
        self.assertEqual(False, ApplicationVersion(1, 2, 3) < ApplicationVersion(1, 2, 3))
        self.assertEqual(True, ApplicationVersion(1, 2, 3) < ApplicationVersion(1, 2, 4))
        self.assertEqual(False, ApplicationVersion(1, 2, 4) < ApplicationVersion(1, 2, 3))

        self.assertEqual(False, ApplicationVersion(1, 2, 3) < ApplicationVersion(1, 2, 3, "SNAPSHOT"))
        self.assertEqual(True, ApplicationVersion(1, 2, 3) < ApplicationVersion(1, 2, 4, "SNAPSHOT"))
        self.assertEqual(False, ApplicationVersion(1, 2, 4) < ApplicationVersion(1, 2, 3, "SNAPSHOT"))

        self.assertEqual(True, ApplicationVersion(1, 2, 3, "SNAPSHOT") < ApplicationVersion(1, 2, 3))
        self.assertEqual(True, ApplicationVersion(1, 2, 3, "SNAPSHOT") < ApplicationVersion(1, 2, 4))
        self.assertEqual(False, ApplicationVersion(1, 2, 4, "SNAPSHOT") < ApplicationVersion(1, 2, 3))

        self.assertEqual(False, ApplicationVersion(1, 2, 3, "SNAPSHOT") < ApplicationVersion(1, 2, 3, "SNAPSHOT"))
        self.assertEqual(True, ApplicationVersion(1, 2, 3, "SNAPSHOT") < ApplicationVersion(1, 2, 4, "SNAPSHOT"))
        self.assertEqual(False, ApplicationVersion(1, 2, 4, "SNAPSHOT") < ApplicationVersion(1, 2, 3, "SNAPSHOT"))

    def test_le(self):
        self.assertEqual(True, ApplicationVersion(1, 2, 3) <= ApplicationVersion(1, 2, 3))
        self.assertEqual(True, ApplicationVersion(1, 2, 3) <= ApplicationVersion(1, 2, 4))
        self.assertEqual(False, ApplicationVersion(1, 2, 4) <= ApplicationVersion(1, 2, 3))

        self.assertEqual(False, ApplicationVersion(1, 2, 3) <= ApplicationVersion(1, 2, 3, "SNAPSHOT"))
        self.assertEqual(True, ApplicationVersion(1, 2, 3) <= ApplicationVersion(1, 2, 4, "SNAPSHOT"))
        self.assertEqual(False, ApplicationVersion(1, 2, 4) <= ApplicationVersion(1, 2, 3, "SNAPSHOT"))

        self.assertEqual(True, ApplicationVersion(1, 2, 3, "SNAPSHOT") <= ApplicationVersion(1, 2, 3))
        self.assertEqual(True, ApplicationVersion(1, 2, 3, "SNAPSHOT") <= ApplicationVersion(1, 2, 4))
        self.assertEqual(False, ApplicationVersion(1, 2, 4, "SNAPSHOT") <= ApplicationVersion(1, 2, 3))

        self.assertEqual(True, ApplicationVersion(1, 2, 3, "SNAPSHOT") <= ApplicationVersion(1, 2, 3, "SNAPSHOT"))
        self.assertEqual(True, ApplicationVersion(1, 2, 3, "SNAPSHOT") <= ApplicationVersion(1, 2, 4, "SNAPSHOT"))
        self.assertEqual(False, ApplicationVersion(1, 2, 4, "SNAPSHOT") <= ApplicationVersion(1, 2, 3, "SNAPSHOT"))

    def test_gt(self):
        self.assertEqual(False, ApplicationVersion(1, 2, 3) > ApplicationVersion(1, 2, 3))
        self.assertEqual(False, ApplicationVersion(1, 2, 3) > ApplicationVersion(1, 2, 4))
        self.assertEqual(True, ApplicationVersion(1, 2, 4) > ApplicationVersion(1, 2, 3))

        self.assertEqual(True, ApplicationVersion(1, 2, 3) > ApplicationVersion(1, 2, 3, "SNAPSHOT"))
        self.assertEqual(False, ApplicationVersion(1, 2, 3) > ApplicationVersion(1, 2, 4, "SNAPSHOT"))
        self.assertEqual(True, ApplicationVersion(1, 2, 4) > ApplicationVersion(1, 2, 3, "SNAPSHOT"))

        self.assertEqual(False, ApplicationVersion(1, 2, 3, "SNAPSHOT") > ApplicationVersion(1, 2, 3))
        self.assertEqual(False, ApplicationVersion(1, 2, 3, "SNAPSHOT") > ApplicationVersion(1, 2, 4))
        self.assertEqual(True, ApplicationVersion(1, 2, 4, "SNAPSHOT") > ApplicationVersion(1, 2, 3))

        self.assertEqual(False, ApplicationVersion(1, 2, 3, "SNAPSHOT") > ApplicationVersion(1, 2, 3, "SNAPSHOT"))
        self.assertEqual(False, ApplicationVersion(1, 2, 3, "SNAPSHOT") > ApplicationVersion(1, 2, 4, "SNAPSHOT"))
        self.assertEqual(True, ApplicationVersion(1, 2, 4, "SNAPSHOT") > ApplicationVersion(1, 2, 3, "SNAPSHOT"))

    def test_ge(self):
        self.assertEqual(True, ApplicationVersion(1, 2, 3) >= ApplicationVersion(1, 2, 3))
        self.assertEqual(False, ApplicationVersion(1, 2, 3) >= ApplicationVersion(1, 2, 4))
        self.assertEqual(True, ApplicationVersion(1, 2, 4) >= ApplicationVersion(1, 2, 3))

        self.assertEqual(True, ApplicationVersion(1, 2, 3) >= ApplicationVersion(1, 2, 3, "SNAPSHOT"))
        self.assertEqual(False, ApplicationVersion(1, 2, 3) >= ApplicationVersion(1, 2, 4, "SNAPSHOT"))
        self.assertEqual(True, ApplicationVersion(1, 2, 4) >= ApplicationVersion(1, 2, 3, "SNAPSHOT"))

        self.assertEqual(False, ApplicationVersion(1, 2, 3, "SNAPSHOT") >= ApplicationVersion(1, 2, 3))
        self.assertEqual(False, ApplicationVersion(1, 2, 3, "SNAPSHOT") >= ApplicationVersion(1, 2, 4))
        self.assertEqual(True, ApplicationVersion(1, 2, 4, "SNAPSHOT") >= ApplicationVersion(1, 2, 3))

        self.assertEqual(True, ApplicationVersion(1, 2, 3, "SNAPSHOT") >= ApplicationVersion(1, 2, 3, "SNAPSHOT"))
        self.assertEqual(False, ApplicationVersion(1, 2, 3, "SNAPSHOT") >= ApplicationVersion(1, 2, 4, "SNAPSHOT"))
        self.assertEqual(True, ApplicationVersion(1, 2, 4, "SNAPSHOT") >= ApplicationVersion(1, 2, 3, "SNAPSHOT"))


class FromFileTestCase(TestCase):
    pass



#class FromStringTestCase(TestCase):
#
#    def test(self):
#        self.assertEqual(
#            ApplicationVersion(1, 2, 3, "SNAPSHOT"),
#            _from_version_string("1.2.3-SNAPSHOT"))
#        self.assertEqual(
#            ApplicationVersion(1, 2, 3, "Alpha"),
#            _from_version_string("1.2.3-Alpha"))
#
#    def test_from_version_string(self):
#        self.assertEqual(
#            "1.2.3",
#            str(from_version_string("1.2.3")))
#        self.assertEqual(
#            "1.2.3-SNAPSHOT",
#            str(from_version_string("1.2.3-SNAPSHOT")))
#        self.assertEqual(
#            "1.2.3-Alpha",
#            str(from_version_string("1.2.3-Alpha")))
#
#    def test_from_version_string_with_invalid_arguments(self):
#        with self.assertRaises(ValueError):
#            ApplicationVersion.from_version_string("")
#        with self.assertRaises(ValueError):
#            ApplicationVersion.from_version_string("1.2")
#        with self.assertRaises(ValueError):
#            ApplicationVersion.from_version_string("1.2.3-")
#        with self.assertRaises(ValueError):
#            ApplicationVersion.from_version_string("1.2.3.4")
#        with self.assertRaises(ValueError):
#            ApplicationVersion.from_version_string("A.B.C")


class ParseVersionStringTestCase(TestCase):

    def test_with_suffix(self):
        self.assertEqual(
            (1, 2, 3, "SNAPSHOT"),
            parse_version_string("1.2.3-SNAPSHOT"))
        self.assertEqual(
            (10, 20, 30, "SNAPSHOT"),
            parse_version_string("10.20.30-SNAPSHOT"))
        self.assertEqual(
            (1, 2, 3, "Alpha"),
            parse_version_string("1.2.3-Alpha"))
        self.assertEqual(
            (1, 2, 3, "Beta"),
            parse_version_string("1.2.3-Beta"))

    def test_without_suffix(self):
        self.assertEqual(
            (1, 2, 3, None),
            parse_version_string("1.2.3"))
        self.assertEqual(
            (10, 20, 30, None),
            parse_version_string("10.20.30"))

    def test_invalid_version_raised_when_version_string_is_invalid_format(self):
        with self.assertRaises(InvalidVersion):
            parse_version_string("")
        with self.assertRaises(InvalidVersion):
            parse_version_string("1")
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.")
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.2")
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.2.")
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.2.3-")
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.2.3.SNAPSHOT")
        with self.assertRaises(InvalidVersion):
            parse_version_string(" 1.2.3")
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.2.3 ")

    def test_invalid_version_raised_when_invalid_major_version_passed(self):
        with self.assertRaises(InvalidVersion):
            parse_version_string(".2.3")
        with self.assertRaises(InvalidVersion):
            parse_version_string("A.2.3")
        with self.assertRaises(InvalidVersion):
            parse_version_string("01.2.3")

    def test_invalid_version_raised_when_invalid_minor_version_passed(self):
        with self.assertRaises(InvalidVersion):
            parse_version_string("1..3")
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.B.3")
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.02.3")

    def test_invalid_version_raised_when_invalid_patch_version_passed(self):
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.2.")
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.2.C")
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.2.03")

    def test_invalid_version_raised_when_invalid_suffix_passed(self):
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.2.3-")
        with self.assertRaises(InvalidVersion):
            parse_version_string("1.2.3--SNAPSHOT")


class BuildVersionStringTestCase(TestCase):

    def test_with_suffix(self):
        self.assertEqual("1.2.3-Alpha", build_version_string(1, 2, 3, "Alpha"))
        self.assertEqual("1.2.3-Beta", build_version_string(1, 2, 3, "Beta"))

    def test_without_suffix(self):
        self.assertEqual("0.0.0", build_version_string(0, 0, 0))
        self.assertEqual("1.2.3", build_version_string(1, 2, 3))
        self.assertEqual("4.5.6", build_version_string(4, 5, 6))
        self.assertEqual("12.34.56", build_version_string(12, 34, 56))

    def test_invalid_version_raised_when_invalid_major_version_passed(self):
        with self.assertRaises(InvalidVersion):
            build_version_string(-1, 2, 3)

    def test_invalid_version_raised_when_invalid_minor_version_passed(self):
        with self.assertRaises(InvalidVersion):
            build_version_string(1, -2, 3)

    def test_invalid_version_raised_when_invalid_patch_version_passed(self):
        with self.assertRaises(InvalidVersion):
            build_version_string(1, 2, -3)

    def test_invalid_version_raised_when_invalid_suffix_passed(self):
        with self.assertRaises(InvalidVersion):
            build_version_string(1, 2, 3, "")
        with self.assertRaises(InvalidVersion):
            build_version_string(1, 2, 3, "-")
        with self.assertRaises(InvalidVersion):
            build_version_string(1, 2, 3, "A-B")


class ToCompareKeyTestCase(TestCase):

    def test_with_suffix(self):
        self.assertEqual(
            (1, 2, 3, False, "Alpha"),
            to_compare_key(ApplicationVersion(1, 2, 3, "Alpha")))
        self.assertEqual(
            (1, 2, 3, False, "Beta"),
            to_compare_key(ApplicationVersion(1, 2, 3, "Beta")))

    def test_without_suffix(self):
        self.assertEqual(
            (0, 0, 0, True, "None"),
            to_compare_key(ApplicationVersion(0, 0, 0)))
        self.assertEqual(
            (1, 2, 3, True, "None"),
            to_compare_key(ApplicationVersion(1, 2, 3)))


if __name__ == "__main__":
    unittest.main()

