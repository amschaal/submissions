"""Aggie Enterprise chartstring formats.

Segment patterns come from the Aggie Enterprise GraphQL schema (GlSegmentString, PpmSegmentString
and their segment scalars).
"""
import re
from collections import namedtuple

GL = 'GL'
PPM = 'PPM'

# (label, pattern) for each segment, in string order.  GL strings need the first four segments and
# may leave off any after that; the last three are unused and always zero.
GL_SEGMENTS = (
    ('Entity', '[0-9]{3}[0-9AB]'),
    ('Fund', '[0-9A-Z]{5}'),
    ('Financial Department', '[0-9A-Z]{7}'),
    ('Account', '[0-9A-Z]{6}'),
    ('Purpose', '[0-9][0-9A-Z]'),
    ('Program', '[0-9A-Z]{3}'),
    ('Project', '[0-9A-Z]{10}'),
    ('Activity', '[0-9A-Z]{6}'),
    ('Inter-Entity', '0000'),
    ('Flex 1', '000000'),
    ('Flex 2', '000000'),
)
# Aggie Enterprise fills unused GL segments with zeroes.
GL_UNUSED = ('00', '000', '0000000000', '000000', '0000', '000000', '000000')
# PPM strings have the four required segments, or all six.
PPM_SEGMENTS = (
    ('Project', '[0-9A-Z]{10}'),
    ('Task', '[0-9A-Z]{6}'),
    ('Organization', '[0-9A-Z]{7}'),
    ('Expenditure Type', '[0-9A-Z]{6}'),
    ('Award', '[0-9A-Z]{7}'),
    ('Funding Source', '[0-9A-Za-z]{5,10}'),
)
GL_FORMAT = ('Entity-Fund-Financial Department-Account (XXXX-XXXXX-XXXXXXX-XXXXXX), '
             'optionally followed by Purpose-Program-Project-Activity')
PPM_FORMAT = ('Project-Task-Organization-Expenditure Type (XXXXXXXXXX-XXXXXX-XXXXXXX-XXXXXX), '
              'optionally followed by Award-Funding Source')

Chartstring = namedtuple('Chartstring', 'kind string')


def parse(value):
    """Parse a GL or PPM chartstring into its canonical form.

    Whitespace is ignored and codes are upper-cased.  PPM strings in POET order
    (Project-Organization-Expenditure Type-Task) are put in the order Aggie Enterprise uses
    (Project-Task-Organization-Expenditure Type), and an all-zero Award and Funding Source
    (placeholders for none) are dropped.  Raises ValueError, with a message for the user, if
    value is neither.
    """
    parts = re.sub(r'\s', '', value or '').strip('-').split('-')
    if len(parts[0]) == 4:
        return parse_gl([part.upper() for part in parts])
    if len(parts[0]) == 10:
        return parse_ppm(parts)
    raise ValueError(f'Please enter a GL chartstring, {GL_FORMAT}, or a PPM chartstring, {PPM_FORMAT}.')


def parse_gl(parts):
    if not 4 <= len(parts) <= len(GL_SEGMENTS):
        raise ValueError(f'A GL chartstring is {GL_FORMAT}.')
    return check(GL, parts, GL_SEGMENTS, GL_FORMAT)


def parse_ppm(parts):
    if len(parts) not in (4, 6):
        raise ValueError(f'A PPM chartstring is {PPM_FORMAT}.')
    # Funding sources may contain lower case letters; every other code is upper case.
    parts = [part.upper() for part in parts[:5]] + parts[5:]
    if len(parts[1]) == 7:  # POET order: an Organization is 7 characters, a Task never is
        parts[1:4] = parts[3], parts[1], parts[2]
    if len(parts) == 6 and not parts[4].strip('0') and not parts[5].strip('0'):
        parts = parts[:4]
    return check(PPM, parts, PPM_SEGMENTS, PPM_FORMAT)


def check(kind, parts, segments, expected):
    for part, (label, pattern) in zip(parts, segments):
        if not re.fullmatch(pattern, part):
            raise ValueError(f'"{part}" is not a valid {label}. A {kind} chartstring is {expected}.')
    return Chartstring(kind, '-'.join(parts))


def complete_gl(string):
    """The full 11 segment form of a GL chartstring that may leave off its optional segments."""
    parts = string.split('-')
    return '-'.join(parts + list(GL_UNUSED[len(parts) - 4:]))
