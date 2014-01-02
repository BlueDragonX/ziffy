import exifread
import re
from .utils import AddressableDict
from collections import defaultdict
from datetime import datetime


class TagSet(AddressableDict):
    """A set of image tags."""
    _datetime_pattern = re.compile(r'^[0-9]{4}:[0-9]{2}:[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$')
    _datetime_format = '%Y:%m:%d %H:%M:%S'

    def __getattr__(self, key):
        """Return a parsed tag value."""
        tag = AddressableDict.__getattr__(self, key)
        value = tag.values
        if self._datetime_pattern.match(tag.printable):
            value = datetime.strptime(value, self._datetime_format)
        return value


class Tags(AddressableDict):
    """A set of tag sets."""

    @classmethod
    def read(cls, filename):
        """Return a Tags object from a file."""
        with open(filename) as f:
            exif = exifread.process_file(f)
        data = defaultdict(lambda: {})
        for key, tag in exif.iteritems():
            if not isinstance(tag, exifread.classes.IfdTag):
                continue
            parts = key.split(' ', 1)
            if len(parts) > 1:
                cat, key = tuple(parts)
                data[cat][key] = tag
        return cls(data)

    def put(self, key, value):
        """Set a TagSet in the Tags object."""
        if not isinstance(value, TagSet):
            value = TagSet(value)
        AddressableDict.put(self, key, value)
