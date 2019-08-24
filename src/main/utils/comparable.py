

class Comparable(type):
    """
        大小比較する compare メソッドから比較演算子を自動生成するメタクラス.
    """

    def __new__(self, name, bases, namespace, **kwargs):
        Comparable.define_compare_methods(namespace)
        return super(Comparable, self).__new__(self, name, bases, namespace, **kwargs)

    @staticmethod
    def define_compare_methods(namespace):
        namespace["__eq__"] = lambda self, other: self.compare(other) == 0
        namespace["__ne__"] = lambda self, other: self.compare(other) != 0
        namespace["__lt__"] = lambda self, other: self.compare(other) < 0
        namespace["__le__"] = lambda self, other: self.compare(other) <= 0
        namespace["__gt__"] = lambda self, other: self.compare(other) > 0
        namespace["__ge__"] = lambda self, other: self.compare(other) >= 0


def comparable(target="compare"):
    """
        大小比較するメソッドから比較演算子を自動生成するデコレータ.
    """

    def define_compare_methods(target_class, compare):
        target_class.__eq__ = lambda self, other: compare(self, other) == 0
        target_class.__ne__ = lambda self, other: compare(self, other) != 0
        target_class.__lt__ = lambda self, other: compare(self, other) < 0
        target_class.__le__ = lambda self, other: compare(self, other) <= 0
        target_class.__gt__ = lambda self, other: compare(self, other) > 0
        target_class.__ge__ = lambda self, other: compare(self, other) >= 0

    if isinstance(target, str):
        def wrapper(target_class):
            compare = target_class.__dict__[target]
            define_compare_methods(target_class, compare)
            return target_class
        return wrapper
    else:
        compare = lambda self, other: self.compare(other)
        define_compare_methods(target, compare)
        return target

