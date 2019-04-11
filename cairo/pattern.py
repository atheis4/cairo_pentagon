# This object must contain all the data necessary to apply a pattern onto a
# layer object.

# What should this look like? Which objects are interacting where to turn the
# individual pentagon's visibility off and on?

# If all a pattern object is doing is turning certain pentagons off and on,
# then all it needs are the keys of the dictionary to turn off.
from cairo.layer import Layer


class Pattern(object):

    _pattern_style = None

    def __int__(self, origin: (int, int)=(0, 0), spin='clockwise'):
        # TODO: origin presents an opportunity to use random input to generate
        # TODO: pattern.
        self.origin_row = origin[0]
        self.origin_column = origin[1]


# TODO: Pattern is applied pentagon by pentagon. We need to traverse the
# TODO: pentagons one by one and turn visibility on.


class SquarePattern(Pattern):

    _pattern_style = 'square'

    def apply(self, shape, orientation, row, column):
