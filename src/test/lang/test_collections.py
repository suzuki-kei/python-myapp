import unittest

from lang.collections import flatten

class CollectionsTestCase(unittest.TestCase):

    def test_flatten(self):
        # no argument
        self.assertEqual([], flatten())

        # None
        self.assertEqual([None], flatten(None))

        # int
        self.assertEqual([1], flatten(1))

        # str
        self.assertEqual([""], flatten(""))
        self.assertEqual(["123"], flatten("123"))

        # range
        self.assertEqual([], flatten(range(0)))
        self.assertEqual([1, 2, 3], flatten(range(1, 4)))

        # list
        self.assertEqual([], flatten([]))
        self.assertEqual([1], flatten([1]))
        self.assertEqual([1, 2], flatten([1, 2]))
        self.assertEqual([1, 2, 3], flatten([1, 2, 3]))
        self.assertEqual([1, 2, 3], flatten([1, 2, [3]]))
        self.assertEqual([1, 2, 3], flatten([1, [2], 3]))
        self.assertEqual([1, 2, 3], flatten([[1], [2], 3]))
        self.assertEqual([1, 2, 3], flatten([1, [2, 3]]))
        self.assertEqual([1, 2, 3], flatten([[1, 2], 3]))
        self.assertEqual([1, 2, 3], flatten([[1, 2, 3]]))

        # tuple
        self.assertEqual([], flatten(()))
        self.assertEqual([1], flatten((1, )))
        self.assertEqual([1, 2], flatten((1, 2)))
        self.assertEqual([1, 2, 3], flatten((1, 2, 3)))
        self.assertEqual([1, 2, 3], flatten((1, 2, 3)))
        self.assertEqual([1, 2, 3], flatten((1, 2, (3))))
        self.assertEqual([1, 2, 3], flatten((1, (2), 3)))
        self.assertEqual([1, 2, 3], flatten(((1), (2), 3)))
        self.assertEqual([1, 2, 3], flatten((1, (2, 3))))
        self.assertEqual([1, 2, 3], flatten(((1, 2), 3)))
        self.assertEqual([1, 2, 3], flatten(((1, 2, 3))))

        # set
        self.assertEqual([], sorted(flatten(set())))
        self.assertEqual([1], sorted(flatten({1})))
        self.assertEqual([1, 2], sorted(flatten({1, 2})))
        self.assertEqual([1, 2, 3], sorted(flatten({1, 2, 3})))

        # dict
        self.assertEqual([dict()], flatten(dict()))
        self.assertEqual([{"one": 1}], flatten({"one": 1}))

        # mixed
        values = [1, [2, 3, (4, {5}, [6])], range(7, 9), {"nine": 9}]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, {"nine": 9}]
        self.assertEqual(expected, flatten(*values))
        self.assertEqual(expected, flatten(values))
        self.assertEqual(expected, flatten([values]))
        self.assertEqual(expected, flatten([(values)]))

