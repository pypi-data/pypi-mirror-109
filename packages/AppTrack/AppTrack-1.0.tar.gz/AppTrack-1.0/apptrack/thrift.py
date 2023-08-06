import six
import socket
import struct

_max_signed_port = (1 << 15) - 1
_max_unsigned_port = (1 << 16)
_max_signed_id = (1 << 63) - 1
_max_unsigned_id = (1 << 64)

if six.PY3:
    long = int

class Tag:
    def __init__(self, key=None, vStr=None):
        self.key = key
        self.vStr = vStr


class Log(object):
    def __init__(self, timestamp=None, fields=None,):
        self.timestamp = timestamp
        self.fields = fields


def ipv4_to_int(ipv4):
    if ipv4 == 'localhost':
        ipv4 = '127.0.0.1'
    elif ipv4 == '::1':
        ipv4 = '127.0.0.1'
    try:
        return struct.unpack('!i', socket.inet_aton(ipv4))[0]
    except:
        return 0


def id_to_int(big_id):
    if big_id is None:
        return None
    # thrift defines ID fields as i64, which is signed,
    # therefore we convert large IDs (> 2^63) to negative longs
    if big_id > _max_signed_id:
        big_id -= _max_unsigned_id
    return big_id


def make_string_tag(key, value, max_length):
    if len(value) > max_length:
        value = value[:max_length]
    return Tag(key=key,vStr=value)


def timestamp_micros(ts):
    """
    Convert a float Unix timestamp from time.time() into a long value in microseconds.
    :param ts:
    :return:
    """
    return long(ts * 1000000)


def make_tags(tags, max_length):
    # TODO extend to support non-string tag values
    return [
        make_string_tag(key=k, value=str(v), max_length=max_length)
        for k, v in six.iteritems(tags or {})
    ]


def make_log(timestamp, fields, max_length):
    return Log(
        timestamp=timestamp_micros(ts=timestamp),
        fields=make_tags(tags=fields, max_length=max_length),
    )


