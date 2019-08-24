import unittest

from utils.modules import import_modules


class ImportAllModulesTestCase(unittest.TestCase):

    def test(self):
        # 全てのモジュールがインポート可能であることをテストするとともに,
        # カバレッジ取得時に全モジュールが結果に含まれるようにするためにインポートする.
        self.assertEqual(True, import_modules("src/main") is not None)

