import unittest

from myapp.utilities.application_version import ApplicationVersion

class ApplicationVersionTestCase(unittest.TestCase):

    def test_constructor(self):
        self.assertEqual(
            "1.2.3",
            str(ApplicationVersion(1, 2, 3)))
        self.assertEqual(
            "1.2.3",
            str(ApplicationVersion(1, 2, 3, "")))
        self.assertEqual(
            "1.2.3",
            str(ApplicationVersion(1, 2, 3, None)))
        self.assertEqual(
            "1.2.3-SNAPSHOT",
            str(ApplicationVersion(1, 2, 3, "SNAPSHOT")))
        self.assertEqual(
            "1.2.3-Alpha",
            str(ApplicationVersion(1, 2, 3, "Alpha")))

    def test_from_version_string(self):
        self.assertEqual(
            "1.2.3",
            str(ApplicationVersion.from_version_string("1.2.3")))
        self.assertEqual(
            "1.2.3-SNAPSHOT",
            str(ApplicationVersion.from_version_string("1.2.3-SNAPSHOT")))
        self.assertEqual(
            "1.2.3-Alpha",
            str(ApplicationVersion.from_version_string("1.2.3-Alpha")))

    def test_from_version_string_with_invalid_arguments(self):
        with self.assertRaises(ValueError):
            ApplicationVersion.from_version_string("")
        with self.assertRaises(ValueError):
            ApplicationVersion.from_version_string("1.2")
        with self.assertRaises(ValueError):
            ApplicationVersion.from_version_string("1.2.3-")
        with self.assertRaises(ValueError):
            ApplicationVersion.from_version_string("1.2.3.4")
        with self.assertRaises(ValueError):
            ApplicationVersion.from_version_string("A.B.C")

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

if __name__ == "__main__":
    unittest.main()

