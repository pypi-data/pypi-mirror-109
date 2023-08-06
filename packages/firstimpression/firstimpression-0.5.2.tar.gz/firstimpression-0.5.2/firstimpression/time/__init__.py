import datetime
import time
from firstimpression.xml import get_text_from_element


def get_datetime_object_from_element(element, name, format):
    """ Gets the datetime object of an element (xml) based on name and format

    :param element: the element from which the date needs to be grabbed
    :type element: xml.etree.ElementTree.Element

    :param name: name of the element in xml which contains date
    :type name: str

    :param format: the format of the datetime in the element
    :type format: str

    :returns: time and date in the right format
    :rtype: date
     """
    unparsed_pubdate = get_text_from_element(element, name)

    created_at = parse_string_to_time(element, format)
    return parse_timestamp_to_date(created_at)


def parse_string_to_time(element, format):
    """ Gets the timestamp of an string in specific format

    :param element: string with the time in it
    :type element: str

    :param format: string with the format devined
    :type format: str

    :returns: time as timestamp
    :rtype: float """
    return parse_date_to_time(parse_string_to_date(element, format))


def parse_date_to_time(date_object):
    return time.mktime(date_object.timetuple())


def parse_string_to_date(element, format):
    return datetime.datetime.strptime(element, format)


def parse_timestamp_to_date(timestamp):
    """ Change timestamp to date object

    :param timestamp: the time in POSIX timestamp
    :type timestamp: float

    :returns: the time as a date
    :rtype: date """
    return datetime.datetime.fromtimestamp(timestamp)


def parse_date_to_string(date_object, format):
    return datetime.datetime.strftime(date_object, format)


def parse_string_time_to_minutes(element):
    [hours, minutes, seconds] = element.split(':')

    if seconds > 30:
        minutes += 1

    minutes += hours * 60

    return minutes


def get_month_text(month_number, month_index):
    return{
        1: ['jan', 'januari'],
        2: ['feb', 'februari'],
        3: ['maa', 'maart'],
        4: ['apr', 'april'],
        5: ['mei', 'mei'],
        6: ['jun', 'juni'],
        7: ['jul', 'juli'],
        8: ['aug', 'augustus'],
        9: ['sep', 'september'],
        10: ['okt', 'oktober'],
        11: ['nov', 'november'],
        12: ['dec', 'december']
    }[month_number][month_index]


def parse_date_to_string_full_day_month(date_object, month_type):
    day = str(date_object.day)
    month = get_month_text(date_object.month, month_type)
    return ' '.join([day, month, parse_date_to_string(date_object, '%Y %H:%M')])
