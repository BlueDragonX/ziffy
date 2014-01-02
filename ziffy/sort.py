import argparse
import os
import signal
import sys
from .tags import Tags
from collections import OrderedDict


default_format = '{{EXIF.DateTimeOriginal:%Y{sep}%m - %B{sep}%d}}'.format(sep=os.sep)
default_unknown = 'Unknown'


class Sorter(object):
    """Image sorter. Uses EXIF data to put images in particular directories."""

    def __init__(self, destination_format, unknown_destination):
        """Create a sorter using the given destination format and destination for unknown images."""
        self.destination_format = destination_format
        self.unknown_destination = unknown_destination

    def order(self, destination_base, source_files):
        """
        Yield a list of (source, destination) tuples describing the move operations that should
        occur.
        """
        if not os.path.isabs(destination_base):
            destination_base = os.path.abspath(destination_base)
        destination_files = set()

        for source in source_files:
            if not os.path.isabs(source):
                source = os.path.abspath(source)
            if not os.path.exists(source):
                continue

            base = os.path.basename(source)
            name, ext = os.path.splitext(base)

            tags = Tags.read(source)
            try:
                destination_path = tags.format(self.destination_format)
            except (AttributeError, KeyError):
                destination_path = self.unknown_destination

            index = 1
            destination_path = os.path.join(destination_base, destination_path)
            destination = os.path.join(destination_path, base)

            while os.path.exists(destination) or destination in destination_files:
                destination = os.join(destination_path, '{}_{:03d}.{}'.format(name, index, ext))
                index += 1

            destination_files.add(destination)
            yield (source, destination)

    def move(self, destination_base, source_files):
        """Move image files to their ordered destination and yield the moves as they complete."""
        for source, destination in self.order(destination_base, source_files):
            destination_path = os.path.dirname(destination)
            if not os.path.isdir(destination_path):
                os.makedirs(destination_path)
            os.rename(source, destination)
            yield(source, destination)


def read_config():
    """Read CLI configuration."""
    parser = argparse.ArgumentParser(description="Organize images based on EXIF data.")
    parser.add_argument(
        '-p', '--pretend', dest='pretend', action='store_true', default=False,
        help="Only show what would be done.")
    parser.add_argument(
        '-q', '--quiet', dest='quiet', action='store_true', default=False,
        help="Don't produce any output.")
    parser.add_argument(
        '-f', '--format', dest='format', nargs=1, default=[default_format],
        help="Destination subdirectory format.")
    parser.add_argument(
        '-u', '--unknown', dest='unknown', nargs=1, default=[default_unknown],
        help="Destination subdirectory for unknown files.")
    parser.add_argument(
        '-d', '--destination', dest='destination', nargs=1, default=['.'],
        help="Base destionation directory.")
    parser.add_argument('images', metavar='image', nargs='*', default=sys.stdin, help="Image to move.")
    config = parser.parse_args()
    config.images = [image.rstrip('\n') for image in config.images]
    config.format = config.format[0]
    config.unknown = config.unknown[0]
    config.destination = config.destination[0]
    return config


def organize(config):
    """Use the provided configuration to move images around."""
    sorter = Sorter(config.format, config.unknown)
    if config.pretend:
        moves = sorter.order(config.destination, config.images)
    else:
        moves = sorter.move(config.destination, config.images)
    for source, destination in moves:
        if not config.quiet:
            print("{} -> {}".format(repr(source), repr(destination)))


def main():
    """Use the sorter to organize some image files."""
    try:
        organize(read_config())
    except KeyboardInterrupt:
        pass
