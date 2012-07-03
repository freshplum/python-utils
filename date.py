import datetime
from dateutil import parser, tz

from . import fill

LONG_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
SHORT_TIMESTAMP_FORMAT = "%Y-%m-%d"

def deserialize_timestamp(dt_string, *args, **kwargs):
    """
    Takes a timestamp string and returns a datetime object.

    This function parses a datetime object from a timestamp using the
    dateutil.parser.parse method. The parse method could be used directly,
    but this method ensures that certain default settings are passed in
    """
    dt = parser.parse(dt_string, dayfirst=False, yearfirst=True, fuzzy=True)

    # If the timestamp contained some time zone information, convert it to UTC
    # time and remove the tzinfo object from the resultant datetime object.
    if dt.tzinfo:
        dt = dt.astimezone(tz.tzutc())
        # FIXIT: The reason for removing the tzinfo object is that we only deal
        #        with UTC time in our app, so all datetime objects do not have
        #        tzinfo objects. It can cause problems in some places if they do
        #        due to the fact that we are using the datetime objects as dict
        #        keys (specifically, the predict function in stats.py has this
        #        problem and should probably be fixed).
        #
        #        This problem has been recorded as Github Issue #452.
        dt = dt.replace(tzinfo=None)
    # else:
    #     dt = dt.replace(tzinfo=tz.tzutc())

    return dt

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
        'DAY'   : 3,
        'MONTH' : 2,
        'YEAR'  : 1
    }

def floor(dt, granularity='SECOND'):
    """
    Floors (similar to math.floor) the date to nearest day, hour, minute, or second
    """
    g = G[granularity.upper()]
    dt_tuple = list(dt.timetuple())
    date_tuple = dt_tuple[0:3] if g > 3 else fill(dt_tuple[0:g], 1, 3)
    time_tuple = fill(dt_tuple[3:g], 0, 3)
    return datetime.datetime(*(date_tuple + time_tuple))

# TODO: Update the ceil method to work up to the year just like the floor method does
def ceil(dt, granularity='SECOND'):
    """
    Similar to math.ceil.  Rounds time up to nearest day, hour, minute, or second.
    """
    g = G[granularity.upper()]
    d = list(dt.timetuple()[:g])

    #Check if any of the less significant times exist and are not 0
    if any(dt.timetuple()[-g:]):
        #Round up
        d[g-1]+=1

    return datetime.datetime(*d)
