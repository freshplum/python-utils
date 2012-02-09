import datetime

LONG_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
SHORT_TIMESTAMP_FORMAT = "%Y-%m-%d"

def deserialize_timestamp(dt_string, format=LONG_TIMESTAMP_FORMAT, short=False):
    """
    Takes a timestamp string and returns a datetime object.

    short    an optional flag indicating the use of the short format
    format   an optional format string that overrides the default format
    """
    if short:
        format = SHORT_TIMESTAMP_FORMAT
    return datetime.datetime.strptime(dt_string, format)

def serialize_timestamp(dt_object, format=LONG_TIMESTAMP_FORMAT, short=False):
    """
    Takes a datetime object and returns a timestamp string.

    short    an optional flag indicating the use of the short format
    format   an optional format string that overrides the default format
    """
    if short:
        format = SHORT_TIMESTAMP_FORMAT
    return datetime.datetime.strftime(dt_object, format)