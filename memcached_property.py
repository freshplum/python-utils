from django.core.cache import cache
try:
    from plum.settings import ALLOW_CACHING, CACHE_TIMEOUT
except ImportError:
    ALLOW_CACHING = True
    CACHE_TIMEOUT = 60
    
class MemcachedClass(object):
    #_ckey_uid_name = 'ckey_uid'
    def __init__(self, ckey_uid=None):
        pass
        """
        print self.get_ckey_uid
        if not ckey_uid:
            if hasattr(super(MemcachedClass, self), 'get_ckey_uid'):
                self.ckey_uid = getattr(self, 'get_ckey_uid')
            elif hasattr(self, 'id'):
                self.ckey_uid = getattr(self, 'id')
        print self.ckey_uid
        """
    @property
    def ckey(self):
        key = self.__class__.__name__
        if hasattr(self, 'get_ckey_uid'):
            key += ('_%s' % self.get_ckey_uid)
        return key

class MemcachedProperty(object):
    def __init__(self, fget=None, fset=None, fdel=None, name=None, doc=None, ckey='ckey', try_cache=True, dont_cache=False):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.name = name
        self.__doc__ = doc
        self.ckey = ckey
        
        self.try_cache = try_cache
        self.dont_cache = dont_cache
    
    def __get__(self, obj, klass=None):
        if not self.try_cache or not ALLOW_CACHING:
            value = self.fget(obj)
        else:
            value = cache.get(self._ckey(obj))
            if not value:
                value = self.fget(obj)
            else:
                pass
        self._save_to_cache(obj, value)
        return value
    
    def __set__(self, obj, value):
        raise AttributeError, "readonly property"

    def __delete__(self, obj):
        if self.fdel is None:
            cache.delete(obj._ckey)

    def _ckey(self, obj):
        if not hasattr(obj, self.ckey):
            raise AttributeError, 'cache key method does not exist. Tried to find method: '
        ckey = getattr(obj, self.ckey)
        return '%s_%s' % (ckey, self.fget.__name__)

    def _save_to_cache(self, obj, value):
        if not self.dont_cache and ALLOW_CACHING:
            cache.set(self._ckey(obj), value, CACHE_TIMEOUT)
            return True
        return False

    

        