######################################################################
#
# File: b2sdk/utils.py
#
# Copyright 2019 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################

from __future__ import division, print_function
import hashlib
import os
import platform
import re
import shutil
import tempfile

from logfury.v0_1 import DefaultTraceAbstractMeta, DefaultTraceMeta, limit_trace_arguments, disable_trace, trace_call

import six

try:
    import concurrent.futures as futures
except ImportError:
    import futures


def interruptible_get_result(future):
    """
    Wait for the result of a future in a way that can be interrupted
    by a KeyboardInterrupt.

    This is not necessary in Python 3, but is needed for Python 2.

    :param future: a future to get result of
    :type future: Future
    """
    while True:
        try:
            return future.result(timeout=1.0)
        except futures.TimeoutError:
            pass


def b2_url_encode(s):
    """
    URL-encode a unicode string to be sent to B2 in an HTTP header.

    :param s: a unicode string to encode
    :type s: str
    :return: URL-encoded string
    :rtype: str
    """
    return six.moves.urllib.parse.quote(s.encode('utf-8'))


def b2_url_decode(s):
    """
    Decode a Unicode string returned from B2 in an HTTP header.

    :param s: a unicode string to decode
    :type s: str
    :return: a Python unicode string.
    :rtype: str
    """
    result = six.moves.urllib.parse.unquote_plus(s)
    if six.PY2:
        # The behavior of unquote_plus is different in python 2 and 3.
        # In Python 3, it decodes the UTF-8, while in Python 2 it does not.
        result = result.decode('utf-8')
    return result


def choose_part_ranges(content_length, minimum_part_size):
    """
    Return a list of (offset, length) for the parts of a large file.

    :param content_length: content length value
    :type content_length: int
    :param minimum_part_size: a minimum file part size
    :type minimum_part_size: int
    :rtype: list
    """

    # If the file is at least twice the minimum part size, we are guaranteed
    # to be able to break it into multiple parts that are all at least
    # the minimum part size.
    assert minimum_part_size * 2 <= content_length

    # How many parts can we make?
    part_count = min(content_length // minimum_part_size, 10000)
    assert 2 <= part_count

    # All of the parts, except the last, are the same size.  The
    # last one may be bigger.
    part_size = content_length // part_count
    last_part_size = content_length - (part_size * (part_count - 1))
    assert minimum_part_size <= last_part_size

    # Make all of the parts except the last
    parts = [(i * part_size, part_size) for i in six.moves.range(part_count - 1)]

    # Add the last part
    start_of_last = (part_count - 1) * part_size
    last_part = (start_of_last, content_length - start_of_last)
    parts.append(last_part)

    return parts


def hex_sha1_of_stream(input_stream, content_length):
    """
    Return the 40-character hex SHA1 checksum of the first content_length
    bytes in the input stream.

    :param input_stream: stream object, which exposes read() method
    :param content_length: expected length of the stream
    :type content_length: int
    :rtype: str
    """
    remaining = content_length
    block_size = 1024 * 1024
    digest = hashlib.sha1()
    while remaining != 0:
        to_read = min(remaining, block_size)
        data = input_stream.read(to_read)
        if len(data) != to_read:
            raise ValueError(
                'content_length(%s) is more than the size of the file' % content_length
            )
        digest.update(data)
        remaining -= to_read
    return digest.hexdigest()


def hex_sha1_of_bytes(data):
    """
    Return the 40-character hex SHA1 checksum of the data.

    :param data: an array of bytes
    :type data: bytes
    :rtype: str
    """
    return hashlib.sha1(data).hexdigest()


def validate_b2_file_name(name):
    """
    Raise a ValueError if the name is not a valid B2 file name.

    :param name: a string to check
    :type name: str
    """
    if not isinstance(name, six.string_types):
        raise ValueError('file name must be a string, not bytes')
    name_utf8 = name.encode('utf-8')
    if len(name_utf8) < 1:
        raise ValueError('file name too short (0 utf-8 bytes)')
    if 1000 < len(name_utf8):
        raise ValueError('file name too long (more than 1000 utf-8 bytes)')
    if name[0] == '/':
        raise ValueError("file names must not start with '/'")
    if name[-1] == '/':
        raise ValueError("file names must not end with '/'")
    if '\\' in name:
        raise ValueError("file names must not contain '\\'")
    if '//' in name:
        raise ValueError("file names must not contain '//'")
    if chr(127) in name:
        raise ValueError("file names must not contain DEL")
    if any(250 < len(segment) for segment in name_utf8.split(six.b('/'))):
        raise ValueError("file names segments (between '/') can be at most 250 utf-8 bytes")


def is_file_readable(local_path, reporter=None):
    """
    Check if the local file has read permissions.

    :param local_path: a file path
    :type local_path: str
    :param reporter: reporter object to put errors on
    :rtype: bool
    """
    if not os.path.exists(local_path):
        if reporter is not None:
            reporter.local_access_error(local_path)
        return False
    elif not os.access(local_path, os.R_OK):
        if reporter is not None:
            reporter.local_permission_error(local_path)
        return False
    return True


def fix_windows_path_limit(path):
    """
    Prefix paths when running on Windows to overcome 260 character path length limit.
    See https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247(v=vs.85).aspx#maxpath

    :param path: a path to prefix
    :type path: str
    :return: a prefixed path
    :rtype: str
    """
    if platform.system() == 'Windows':
        if path.startswith('\\\\'):
            # UNC network path
            return '\\\\?\\UNC\\' + path[2:]
        elif os.path.isabs(path):
            # local absolute path
            return '\\\\?\\' + path
        else:
            # relative path, don't alter
            return path
    else:
        return path


class BytesIoContextManager(object):
    """
    A simple wrapper for a BytesIO that makes it look like
    a file-like object that can be a context manager.
    """

    def __init__(self, byte_data):
        """
        :param bytes_data: a byte stream
        """
        self.byte_data = byte_data

    def __enter__(self):
        return six.BytesIO(self.byte_data)

    def __exit__(self, type_, value, traceback):
        return None  # don't hide exception


class TempDir(object):
    """
    Context manager that creates and destroys a temporary directory.
    """

    def __enter__(self):
        """
        Return the unicode path to the temp dir.
        """
        dirpath_bytes = tempfile.mkdtemp()
        self.dirpath = six.u(dirpath_bytes.replace('\\', '\\\\'))
        return self.dirpath

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.dirpath)
        return None  # do not hide exception


def _pick_scale_and_suffix(x):
    # suffixes for different scales
    suffixes = ' kMGTP'

    # We want to use the biggest suffix that makes sense.
    ref_digits = str(int(x))
    index = (len(ref_digits) - 1) // 3
    suffix = suffixes[index]
    if suffix == ' ':
        suffix = ''

    scale = 1000**index
    return (scale, suffix)


def format_and_scale_number(x, unit):
    """
    Pick a good scale for representing a number and format it.

    :param x: a number
    :type x: int
    :param unit: an arbitrary unit name
    :type unit: str
    :return: scaled and formatted number
    :rtype: str
    """

    # simple case for small numbers
    if x < 1000:
        return '%d %s' % (x, unit)

    # pick a scale
    (scale, suffix) = _pick_scale_and_suffix(x)

    # decide how many digits after the decimal to display
    scaled = x / scale
    if scaled < 10.0:
        fmt = '%1.2f %s%s'
    elif scaled < 100.0:
        fmt = '%1.1f %s%s'
    else:
        fmt = '%1.0f %s%s'

    # format it
    return fmt % (scaled, suffix, unit)


def format_and_scale_fraction(numerator, denominator, unit):
    """
    Pick a good scale for representing a fraction, and format it.

    :param numerator: a numerator of a fraction
    :type numerator: int
    :param denominator: a denominator of a fraction
    :type denominator: int
    :param unit: an arbitrary unit name
    :type unit: str
    :return: scaled and formatted fraction
    :rtype: str
    """

    # simple case for small numbers
    if denominator < 1000:
        return '%d / %d %s' % (numerator, denominator, unit)

    # pick a scale
    (scale, suffix) = _pick_scale_and_suffix(denominator)

    # decide how many digits after the decimal to display
    scaled_denominator = denominator / scale
    if scaled_denominator < 10.0:
        fmt = '%1.2f / %1.2f %s%s'
    elif scaled_denominator < 100.0:
        fmt = '%1.1f / %1.1f %s%s'
    else:
        fmt = '%1.0f / %1.0f %s%s'

    # format it
    scaled_numerator = numerator / scale
    return fmt % (scaled_numerator, scaled_denominator, suffix, unit)


_CAMELCASE_TO_UNDERSCORE_RE = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')


def camelcase_to_underscore(input_):
    """
    Convert a camel-cased string to a string with underscores.

    :param input_: an input string
    :type input_: str
    :return: string with underscores
    :rtype: str
    """
    return _CAMELCASE_TO_UNDERSCORE_RE.sub(r'_\1', input_).lower()


class B2TraceMeta(DefaultTraceMeta):
    """
    Trace all public method calls, except for ones with names that begin with `get_`.
    """
    pass


class B2TraceMetaAbstract(DefaultTraceAbstractMeta):
    """
    Default class for tracers, to be set as
    a metaclass for abstract base classes.
    """
    pass


assert disable_trace
assert limit_trace_arguments
assert trace_call
