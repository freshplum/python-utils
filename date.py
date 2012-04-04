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

G = {
        'SECOND': 6,
        'MINUTE': 5,
        'HOUR'  : 4,
        'DAY'   : 3
    }

def floor(dt, granularity):
    """
    Floors (similar to math.floor) the date to nearest day, hour, minute, or second
    """
    g = G.get(granularity.upper(), 6)
    return datetime.datetime(*dt.timetuple()[0:g])


def ceil(dt, granularity):
    """
    Similar to math.ceil.  Rounds time up to nearest day, hour, minute, or second.
    """
    g = G.get(granularity.upper(), 6)
    d = list(dt.timetuple()[:g])

    #Check if any of the less significant times exist and are not 0
    if any(dt.timetuple()[-g:]):
        #Round up
        d[g-1]+=1
        
    return datetime.datetime(*d)
    
