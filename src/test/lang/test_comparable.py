import unittest

from lang.comparable import comparable
from lang.comparable import Comparable

class ComparableTestCase(unittest.TestCase):

    def test_metaclass_with_slots(self):
        class ComparableClass(object, metaclass=Comparable):
            __slots__ = ('_value', )
            def __init__(self, value):
                self._value = value
            def compare(self, other):
                if not isinstance(other, self.__class__):
                    return NotImplemented
                return self._value - other._value
        self._test_compare_methods(ComparableClass)

    def test_metaclass_without_slots(self):
        class ComparableClass(object, metaclass=Comparable):
            def __init__(self, value):
                self._value = value
            def compare(self, other):
                if not isinstance(other, self.__class__):
                    return NotImplemented
                return self._value - other._value
        self._test_compare_methods(ComparableClass)

    def test_decorator_with_args_and_with_slots(self):
        @comparable("compare_to")
        class ComparableClass(object):
            __slots__ = ('_value', )
            def __init__(self, value):
                self._value = value
            def compare_to(self, other):
                if not isinstance(other, self.__class__):
                    return NotImplemented
                return self._value - other._value
        self._test_compare_methods(ComparableClass)

    def test_decorator_with_args_and_without_slots(self):
        @comparable("compare_to")
        class ComparableClass(object):
            def __init__(self, value):
                self._value = value
            def compare_to(self, other):
                if not isinstance(other, self.__class__):
                    return NotImplemented
                return self._value - other._value
        self._test_compare_methods(ComparableClass)

    def test_decorator_without_args_and_with_slots(self):
        @comparable
        class ComparableClass(object):
            __slots__ = ('_value', )
            def __init__(self, value):
                self._value = value
            def compare(self, other):
                if not isinstance(other, self.__class__):
                    return NotImplemented
                return self._value - other._value
        self._test_compare_methods(ComparableClass)

    def test_decorator_without_args_and_without_slots(self):
        @comparable
        class ComparableClass(object):
            def __init__(self, value):
                self._value = value
            def compare(self, other):
                if not isinstance(other, self.__class__):
                    return NotImplemented
                return self._value - other._value
        self._test_compare_methods(ComparableClass)

    def _test_compare_methods(self, comparable_class):
        self.assertEqual(False, comparable_class(0) == comparable_class(1))
        self.assertEqual(True, comparable_class(1) == comparable_class(1))
        self.assertEqual(False, comparable_class(2) == comparable_class(1))

        self.assertEqual(True, comparable_class(0) != comparable_class(1))
        self.assertEqual(False, comparable_class(1) != comparable_class(1))
        self.assertEqual(True, comparable_class(2) != comparable_class(1))

        self.assertEqual(False, comparable_class(0) > comparable_class(1))
        self.assertEqual(False, comparable_class(1) > comparable_class(1))
        self.assertEqual(True, comparable_class(2) > comparable_class(1))

        self.assertEqual(False, comparable_class(0) >= comparable_class(1))
        self.assertEqual(True, comparable_class(1) >= comparable_class(1))
        self.assertEqual(True, comparable_class(2) >= comparable_class(1))

        self.assertEqual(True, comparable_class(0) < comparable_class(1))
        self.assertEqual(False, comparable_class(1) < comparable_class(1))
        self.assertEqual(False, comparable_class(2) < comparable_class(1))

        self.assertEqual(True, comparable_class(0) <= comparable_class(1))
        self.assertEqual(True, comparable_class(1) <= comparable_class(1))
        self.assertEqual(False, comparable_class(2) <= comparable_class(1))

if __name__ == "__main__":
    unittest.main()

