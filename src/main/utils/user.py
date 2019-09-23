from datetime import date
from datetime import timedelta


def full_name(family_name: str, given_name: str, separator=" ") -> str:
    """
        姓 (family_name) と名 (given_name) を連結し, フルネームを生成する.

        Arguments
        ---------
        family_name : str
            姓.
        given_name : str
            名.
        separator : str
            姓と名を連結するときのセパレータ.

        Returns
        -------
        full_name : str
            フルネーム.

        Raises
        ------
        ValueError
            family_name が空文字列, または given_name が空文字列の場合.
    """
    if len(family_name) == 0:
        raise ValueError
    if len(given_name) == 0:
        raise ValueError

    return "{}{}{}".format(family_name, separator, given_name)


def time_basis_age(birthday: date, today: date) -> int:
    """
        時刻基準の年齢を求める.

        Arguments
        ---------
        birthday : date
            誕生日.
        today : date
            基準日.

        Returns
        -------
        time_basis_age : int
            today 時点における時刻基準の年齢.

        Raises
        ------
        ValueError
            today < birthday である場合.
    """
    if today < birthday:
        raise ValueError

    to_int = lambda date: int(date.strftime("%Y%m%d"))
    return (to_int(today) - to_int(birthday)) // 10000


def date_basis_age(birthday: date, today: date) -> int:
    """
        日基準の年齢を求める.

        Arguments
        ---------
        birthday : date
            誕生日.
        today : date
            基準日.

        Returns
        -------
        date_basis_age : int
            today 時点における日基準の年齢.

        Raises
        ------
        ValueError
            today < birthday である場合.
    """
    if today < birthday:
        raise ValueError

    tomorrow = today + timedelta(days=1)
    return time_basis_age(birthday, tomorrow)

