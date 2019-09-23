import unittest
from datetime import date

from utils.user import full_name
from utils.user import time_basis_age
from utils.user import date_basis_age


class FullNameTestCase(unittest.TestCase):
    """
        full_name のテストケース.
    """

    def test(self):
        self.assertEqual("jane doe", full_name("jane", "doe"))
        self.assertEqual("python taro", full_name("python", "taro"))
        self.assertEqual("python jiro", full_name("python", "jiro"))

    def test_when_separator_specified(self):
        self.assertEqual("JaneDoe", full_name("Jane", "Doe", separator=""))
        self.assertEqual("Jane-Doe", full_name("Jane", "Doe", separator="-"))

    def test_value_error_raised_when_family_name_is_empty(self):
        with self.assertRaises(ValueError):
            full_name("", "given_name")

    def test_value_error_raised_when_given_name_is_empty(self):
        with self.assertRaises(ValueError):
            full_name("family_name", "")


class TimeBasisAgeTestCase(unittest.TestCase):
    """
        time_basis_age のテストケース.

        正常系として, 誕生日が以下の場合についてテストする.

            * 元旦 (1/1)
            * 閏日 (2/29)
            * 閏日の翌日 (3/1)
            * 大晦日 (12/31)
            * 上記のいずれでもない日 (7/7)

        異常系として以下の場合についてテストする.

            * today < birthday の場合
    """

    def test_when_birthday_is_new_years_day(self):
        self.assertEqual(
            0, time_basis_age(date(2000, 1, 1), date(2000, 1, 1)))
        self.assertEqual(
            0, time_basis_age(date(2000, 1, 1), date(2000, 12, 31)))
        self.assertEqual(
            1, time_basis_age(date(2000, 1, 1), date(2001, 1, 1)))
        self.assertEqual(
            1, time_basis_age(date(2000, 1, 1), date(2001, 12, 31)))
        self.assertEqual(
            2, time_basis_age(date(2000, 1, 1), date(2002, 1, 1)))
        self.assertEqual(
            2, time_basis_age(date(2000, 1, 1), date(2002, 12, 31)))

    def test_when_birthday_is_leap_day(self):
        # 誕生日が閏日の人は, 閏年には 2/29 に歳をとり, 閏年以外では 3/1 に歳をとる.
        self.assertEqual(
            0, time_basis_age(date(2000, 2, 29), date(2000, 2, 29)))
        self.assertEqual(
            0, time_basis_age(date(2000, 2, 29), date(2000, 3, 1)))
        self.assertEqual(
            0, time_basis_age(date(2000, 2, 29), date(2001, 2, 28)))
        self.assertEqual(
            1, time_basis_age(date(2000, 2, 29), date(2001, 3, 1)))
        self.assertEqual(
            1, time_basis_age(date(2000, 2, 29), date(2002, 2, 28)))
        self.assertEqual(
            2, time_basis_age(date(2000, 2, 29), date(2002, 3, 1)))
        self.assertEqual(
            2, time_basis_age(date(2000, 2, 29), date(2003, 2, 28)))
        self.assertEqual(
            3, time_basis_age(date(2000, 2, 29), date(2003, 3, 1)))
        self.assertEqual(
            3, time_basis_age(date(2000, 2, 29), date(2004, 2, 28)))
        self.assertEqual(
            4, time_basis_age(date(2000, 2, 29), date(2004, 2, 29)))
        self.assertEqual(
            4, time_basis_age(date(2000, 2, 29), date(2004, 3, 1)))

    def test_when_birthday_is_tomorrow_of_leap_day(self):
        # 3/1 生まれの人は, 閏年かどうかに関わらず, 3/1 に歳をとる.
        self.assertEqual(
            0, time_basis_age(date(2000, 3, 1), date(2000, 3, 1)))
        self.assertEqual(
            0, time_basis_age(date(2000, 3, 1), date(2001, 2, 28)))
        self.assertEqual(
            1, time_basis_age(date(2000, 3, 1), date(2001, 3, 1)))
        self.assertEqual(
            1, time_basis_age(date(2000, 3, 1), date(2002, 2, 28)))
        self.assertEqual(
            2, time_basis_age(date(2000, 3, 1), date(2002, 3, 1)))
        self.assertEqual(
            2, time_basis_age(date(2000, 3, 1), date(2003, 2, 28)))
        self.assertEqual(
            3, time_basis_age(date(2000, 3, 1), date(2003, 3, 1)))
        self.assertEqual(
            3, time_basis_age(date(2000, 3, 1), date(2004, 2, 29)))
        self.assertEqual(
            4, time_basis_age(date(2000, 3, 1), date(2004, 3, 1)))

    def test_when_birthday_is_normal_day(self):
        self.assertEqual(
            0, time_basis_age(date(2000, 7, 7), date(2000, 7, 7)))
        self.assertEqual(
            0, time_basis_age(date(2000, 7, 7), date(2001, 7, 6)))
        self.assertEqual(
            1, time_basis_age(date(2000, 7, 7), date(2001, 7, 7)))
        self.assertEqual(
            1, time_basis_age(date(2000, 7, 7), date(2002, 7, 6)))
        self.assertEqual(
            2, time_basis_age(date(2000, 7, 7), date(2002, 7, 7)))
        self.assertEqual(
            2, time_basis_age(date(2000, 7, 7), date(2003, 7, 6)))

    def test_when_birthday_is_new_years_eve(self):
        self.assertEqual(
            0, time_basis_age(date(2000, 12, 31), date(2000, 12, 31)))
        self.assertEqual(
            0, time_basis_age(date(2000, 12, 31), date(2001, 12, 30)))
        self.assertEqual(
            1, time_basis_age(date(2000, 12, 31), date(2001, 12, 31)))
        self.assertEqual(
            1, time_basis_age(date(2000, 12, 31), date(2002, 12, 30)))
        self.assertEqual(
            2, time_basis_age(date(2000, 12, 31), date(2002, 12, 31)))
        self.assertEqual(
            2, time_basis_age(date(2000, 12, 31), date(2003, 12, 30)))

    def test_value_error_raised_when_today_less_than_birthday(self):
        with self.assertRaises(ValueError):
            time_basis_age(date(2000, 1, 1), date(1999, 12, 31))
        with self.assertRaises(ValueError):
            time_basis_age(date(2000, 1, 2), date(2000, 1, 1))


class DateBasisAgeTestCase(unittest.TestCase):
    """
        date_basis_age のテストケース.

        正常系として, 誕生日が以下の場合についてテストする.

            * 元旦 (1/1)
            * 閏日 (2/29)
            * 閏日の翌日 (3/1)
            * 大晦日 (12/31)
            * 上記のいずれでもない日 (7/7)

        異常系として以下の場合についてテストする.

            * today < birthday の場合
    """

    def test_when_birthday_is_new_years_day(self):
        self.assertEqual(
            0, date_basis_age(date(2000, 1, 1), date(2000, 12, 30)))
        self.assertEqual(
            1, date_basis_age(date(2000, 1, 1), date(2000, 12, 31)))
        self.assertEqual(
            1, date_basis_age(date(2000, 1, 1), date(2001, 12, 30)))
        self.assertEqual(
            2, date_basis_age(date(2000, 1, 1), date(2001, 12, 31)))
        self.assertEqual(
            2, date_basis_age(date(2000, 1, 1), date(2002, 12, 30)))
        self.assertEqual(
            3, date_basis_age(date(2000, 1, 1), date(2002, 12, 31)))

    def test_when_birthday_is_leap_day(self):
        # 誕生日が閏日の人は, 閏年には 2/28 に歳をとる.
        self.assertEqual(
            0, date_basis_age(date(2000, 2, 29), date(2000, 2, 29)))
        self.assertEqual(
            0, date_basis_age(date(2000, 2, 29), date(2000, 3, 1)))
        self.assertEqual(
            1, date_basis_age(date(2000, 2, 29), date(2001, 2, 28)))
        self.assertEqual(
            1, date_basis_age(date(2000, 2, 29), date(2001, 3, 1)))
        self.assertEqual(
            2, date_basis_age(date(2000, 2, 29), date(2002, 2, 28)))
        self.assertEqual(
            2, date_basis_age(date(2000, 2, 29), date(2002, 3, 1)))
        self.assertEqual(
            3, date_basis_age(date(2000, 2, 29), date(2003, 2, 28)))
        self.assertEqual(
            3, date_basis_age(date(2000, 2, 29), date(2003, 3, 1)))
        self.assertEqual(
            4, date_basis_age(date(2000, 2, 29), date(2004, 2, 28)))
        self.assertEqual(
            4, date_basis_age(date(2000, 2, 29), date(2004, 2, 29)))

    def test_when_birthday_is_tomorrow_of_leap_day(self):
        # 3/1 生まれの人は, 閏年では 2/29 に歳をとり, 閏年以外では 2/28 に歳をとる.
        self.assertEqual(
            0, date_basis_age(date(2000, 3, 1), date(2000, 3, 1)))
        self.assertEqual(
            0, date_basis_age(date(2000, 3, 1), date(2001, 2, 27)))
        self.assertEqual(
            1, date_basis_age(date(2000, 3, 1), date(2001, 2, 28)))
        self.assertEqual(
            1, date_basis_age(date(2000, 3, 1), date(2002, 2, 27)))
        self.assertEqual(
            2, date_basis_age(date(2000, 3, 1), date(2002, 2, 28)))
        self.assertEqual(
            2, date_basis_age(date(2000, 3, 1), date(2003, 2, 27)))
        self.assertEqual(
            3, date_basis_age(date(2000, 3, 1), date(2003, 2, 28)))
        self.assertEqual(
            3, date_basis_age(date(2000, 3, 1), date(2004, 2, 27)))
        self.assertEqual(
            3, date_basis_age(date(2000, 3, 1), date(2004, 2, 28)))
        self.assertEqual(
            4, date_basis_age(date(2000, 3, 1), date(2004, 2, 29)))

    def test_when_birthday_is_normal_day(self):
        self.assertEqual(
            0, date_basis_age(date(2000, 7, 7), date(2000, 7, 7)))
        self.assertEqual(
            1, date_basis_age(date(2000, 7, 7), date(2001, 7, 6)))
        self.assertEqual(
            1, date_basis_age(date(2000, 7, 7), date(2001, 7, 7)))
        self.assertEqual(
            2, date_basis_age(date(2000, 7, 7), date(2002, 7, 6)))
        self.assertEqual(
            2, date_basis_age(date(2000, 7, 7), date(2002, 7, 7)))
        self.assertEqual(
            3, date_basis_age(date(2000, 7, 7), date(2003, 7, 6)))

    def test_when_birthday_is_new_years_eve(self):
        self.assertEqual(
            0, date_basis_age(date(2000, 12, 31), date(2000, 12, 31)))
        self.assertEqual(
            1, date_basis_age(date(2000, 12, 31), date(2001, 12, 30)))
        self.assertEqual(
            1, date_basis_age(date(2000, 12, 31), date(2001, 12, 31)))
        self.assertEqual(
            2, date_basis_age(date(2000, 12, 31), date(2002, 12, 30)))
        self.assertEqual(
            2, date_basis_age(date(2000, 12, 31), date(2002, 12, 31)))
        self.assertEqual(
            3, date_basis_age(date(2000, 12, 31), date(2003, 12, 30)))

    def test_value_error_raised_when_today_less_than_birthday(self):
        with self.assertRaises(ValueError):
            date_basis_age(date(2000, 1, 1), date(1999, 12, 31))
        with self.assertRaises(ValueError):
            date_basis_age(date(2000, 1, 2), date(2000, 1, 1))


if __name__ == "__main__":
    unittest.main()

