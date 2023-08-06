class ObjectProxy:
    """Decorator allowing override of attributes on an instance of another object

    >>> s1 = "hello"
    >>> s2 = ObjectProxy(s1)
    >>> s2.encode = lambda: b"goodbye!"
    >>> assert s1.encode() == b"hello"
    >>> assert s2.encode() == b"goodbye!"
    """

    def __init__(self, inner):
        self.__inner = inner

    def __getattr__(self, name):
        return getattr(self.__inner, name)

    def __call__(self, *args, **kwargs):
        return self.__inner(*args, **kwargs)
