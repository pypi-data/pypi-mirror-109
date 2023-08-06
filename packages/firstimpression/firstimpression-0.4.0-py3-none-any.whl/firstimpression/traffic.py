import geopy
import xml.etree.ElementTree as ET

METER_TO_KILOMETER_DIVIDER = 1000
KILOMETER_APPENDIX = ' km'
UNKNOWN_JAM_DISTANCE_MESSAGE = 'onbekend'
JAM_TYPE = 4

ROAD_TYPE = 'road_type'
ROAD = 'road'
ROAD_NUMBER = 'road_number'
FROM = 'from'
TO = 'to'
LENGTH = 'length'
LENGTH_STRING = 'length_string'
REASON = 'reason'
AREA_DETAIL = 'area_detail'
EVENT = 'event'
DESCRIPTION = 'description'
TYPE = 'type'
AVG_SPEED = 'avg_speed'
TOTAL_DELAY = 'total_delay'
DISTANCE_TO_CIRCUMSTANCES = 'distance_to_circumstance'
COORDINATES = 'coordinates'
CIRCUMSTANCE_NAME = 'item'


def get_road_type(circumstance):
    try:
        return circumstance['roadNumber'][0]
    except KeyError:
        return False


def get_road(circumstance):
    try:
        return circumstance['roadNumber']
    except KeyError:
        return False


def get_road_number(circumstance):
    # Get road number (A or N)
    try:
        return circumstance['roadNumber'][0]
    except KeyError:
        return False


def get_from(circumstance):
    from_location = circumstance['directionText'].split(' - ')
    return from_location[0]


def get_to(circumstance):
    to_location = circumstance['directionText'].split(' - ')
    return to_location[1]


def get_length(circumstance):
    total_length = circumstance.get('total_length', None)
    if total_length is None:
        return ''
    else:
        return int(total_length)


def get_length_string(circumstance):
    length = circumstance.get('total_length', '')
    if length:
        return ''.join([str(int(length / METER_TO_KILOMETER_DIVIDER)), KILOMETER_APPENDIX])
    else:
        return UNKNOWN_JAM_DISTANCE_MESSAGE


def get_reason(circumstance):
    return circumstance.get('cause', '')


def get_area_detail(circumstance):
    return circumstance.get('locationText', '')


def get_event(circumstance):
    return circumstance.get('title', '')


def get_description(circumstance):
    return circumstance.get('description', '')


def get_type(circumstance):
    return circumstance.get('obstructionType', 0)


def get_avg_speed(circumstance):
    return circumstance.get('total_avg_speed', '')


def get_total_delay_string(circumstance):
    # returns string with delay in minutes or False

    total_delay = circumstance.get('delay', '')

    if total_delay:
        # Round up minutes
        return '+{} min'.format(total_delay)
    else:
        return ''


def get_coordinates(circumstance):
    try:
        return {'longitude': circumstance['longitude'],
                'latitude': circumstance['latitude']
                }
    except KeyError:
        return False


def get_distance_to_circumstance(from_coordinates, to_coordinates):
    # Calculates distance from one coordinate to another (WATCH OUT: straight line, so no roads taken into account)
    if not from_coordinates or not to_coordinates:
        return ''

    coords_1 = (from_coordinates['latitude'], from_coordinates['longitude'])
    coords_2 = (to_coordinates['latitude'], to_coordinates['longitude'])

    return geopy.distance.vincenty(coords_1, coords_2).km


def parse_circumstance(circumstance, own_coordinates):
    # Parses JSON from API to own format. Junk data is removed.
    parsed_circumstance = dict()

    parsed_circumstance[ROAD_TYPE] = get_road_type(circumstance)
    parsed_circumstance[ROAD] = get_road(circumstance)
    parsed_circumstance[ROAD_NUMBER] = get_road_number(circumstance)
    parsed_circumstance[FROM] = get_from(circumstance)
    parsed_circumstance[TO] = get_to(circumstance)
    parsed_circumstance[LENGTH] = get_length(circumstance)
    parsed_circumstance[LENGTH_STRING] = ''
    parsed_circumstance[REASON] = get_reason(circumstance)
    parsed_circumstance[AREA_DETAIL] = get_area_detail(circumstance)
    parsed_circumstance[EVENT] = get_event(circumstance)
    parsed_circumstance[DESCRIPTION] = get_description(circumstance)
    parsed_circumstance[TYPE] = get_type(circumstance)
    parsed_circumstance[AVG_SPEED] = get_avg_speed(circumstance)
    parsed_circumstance[TOTAL_DELAY] = get_total_delay_string(circumstance)
    parsed_circumstance[COORDINATES] = get_coordinates(circumstance)

    parsed_circumstance[DISTANCE_TO_CIRCUMSTANCES] = get_distance_to_circumstance(
        own_coordinates, parsed_circumstance[COORDINATES])

    return parsed_circumstance


def parse_circumstances(circumstances, own_coordinates):
    parsed_circumstances = list()
    for circumstance in circumstances:
        parsed_circumstances.append(
            parse_circumstance(circumstance, own_coordinates))
    return parsed_circumstances


def parse_circumstances_to_XML(circumstances, exclude_items):
    # Parses list of json objects to XML
    root = ET.Element("root")
    for circumstance in circumstances:
        item = ET.SubElement(root, CIRCUMSTANCE_NAME)
        for attribute in circumstance:
            if attribute not in exclude_items:
                ET.SubElement(item, attribute).text = str(
                    circumstance[attribute])

    return root


def sort_longest_jams(jams):
    # Sorts longest jams starting with longest to shortest
    return sorted(jams, key=lambda i: i[LENGTH], reverse=True)


def sort_closest_jams(jams):
    # Sorts jams that are closest to own location
    return sorted(jams, key=lambda i: i[DISTANCE_TO_CIRCUMSTANCES])


def get_jams(circumstances):
    # Filters jams from all possible circumstances which could be f.e. road works and/or police controls
    jams = list()
    for circumstance in circumstances:
        # print(json.dumps(circumstance, indent=2))
        if circumstance[TYPE] == JAM_TYPE:
            jams.append(circumstance)
    return jams


def get_total_jam_length(circumstances):
    return circumstances['totalLengthOfJams'] / 1000


def get_total_jams_delay(jams):
    total_delay = 0
    for jam in jams:
        try:
            total_delay += int(jam[TOTAL_DELAY].split(' ').pop(0))
        except (TypeError, ValueError):
            continue
    if total_delay > 60:
        return '{}+ uur'.format(int(total_delay / 60))
    else:
        return '{} min'.format(int(total_delay))


def get_total_length_string(total_length):
    return '{} km'.format(total_length)


def get_only_highways(circumstances):
    specific_circumstances = list()
    for circumstance in circumstances:
        # print(circumstance)
        if circumstance[ROAD_TYPE] == 'A':
            specific_circumstances.append(circumstance)
    return specific_circumstances
