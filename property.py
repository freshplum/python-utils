import re

class CachedProperty(object):
    """
    Creates a property that caches its value in an instance variable
    (i.e., lazy initialization).
    
    >>> import random
    >>> class Foo(object):
    ...    def get_x(self): return random.random()
    ...    x = CachedProperty(get_x)
    >>> foo = Foo()
    >>> x1 = foo.x
    >>> x2 = foo.x
    >>> x1 == x2
    True
    
    You can also use CachedProperty as a decorator.
    
    >>> class Bar(object):
    ...    @CachedProperty
    ...    def random_value(self): return random.random()
    >>> bar = Bar()
    >>> bar.random_value == bar.random_value
    True
    
    However, creating a CachedProperty in this way will create a read only 
    property.
    
    >>> bar.random_value = 10
    Traceback (most recent call last):
    ...
    AttributeError: readonly property
    
    The name argument allows you to override the name of the ivar used for
    caching the value with a name of your own choosing.
    
    >>> class Baz(object):
    ...    def get_value(self): return random.random()
    ...    def set_value(self, value): self._val = value
    ...    value = CachedProperty(fget=get_value, fset=set_value, name='_val')
    >>> baz = Baz()
    >>> val1 = baz.value
    >>> val2 = baz.value
    >>> val1 == val2
    True
    >>> baz.value = -1
    >>> val1 != baz.value
    True
    
    Using the CachedProperty descriptor gives you delete functionality for
    free. Calling the `del` function on the property will remove it from the 
    instance's __dict__ essentially clearing the cache.
    
    >>> old = baz.value
    >>> del baz.value
    >>> new = baz.value
    >>> old != new
    True
    """
    
    def __init__(self, fget=None, fset=None, fdel=None, name=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.name = name or self._ivar_name(fget.__name__ or fset.__name__)
        self.__doc__ = doc
    
    def __get__(self, obj, klass=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError, "unreadable attribute"
        if not hasattr(obj, self.name):
            value = self.fget(obj)
            setattr(obj, self.name, value)
        return getattr(obj, self.name)
        
    def __set__(self, obj, value):
        if obj is None:
            return self
        if self.fset is None:
            raise AttributeError, "readonly property"
        self.fset(obj, value)
        
    def __delete__(self, obj):
        if self.fdel is None:
            if hasattr(obj, self.name):
                delattr(obj, self.name)
        
    def _ivar_name(self, name):
        """
        Creates the ivar name to be used for caching this property's value 
        on the instance object. It tries to extract a variable name from the
        given name by removing any 'get' or 'set' prefixes and prefixing an
        underscore to specify that the variable should be considered private.
        """
        m = re.match('^_*[gGsS]et_?(.+)$', name)
        if m:
            return '_' + m.group(1)
        return '_' + name
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()