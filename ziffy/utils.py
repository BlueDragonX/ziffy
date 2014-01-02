import re


class AddressableDict(object):
    """
    An object whose values are backed by a dictionary. Key names are normalized to conform to
    Python variable name conventions.
    """
    _disallow = re.compile(r'[^a-zA-Z0-9_]')
    _replace = ''

    def __init__(self, data={}):
        self._data = {}
        for key, value in data.iteritems():
            self.put(key, value)

    def __getattr__(self, key):
        """Return a value in the dictionary."""
        if key not in self._data:
            msg = "'{}' object has no attribute '{}'".format(self.__class__.__name__, key)
            raise AttributeError(msg)
        return self._data[key]

    def put(self, key, value):
        """Set a value in the dictionary."""
        self._data[self._disallow.sub(self._replace, key)] = value

    def keys(self):
        return self._data.keys()

    def format(self, fmt, *args, **kwargs):
        """Return a string formatted with the contents of this object."""
        context = dict(self._data)
        if kwargs:
            context.update(kwargs)
        return fmt.format(*args, **context)
