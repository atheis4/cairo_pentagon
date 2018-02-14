
class Origin(object):
    """The origin object begins the spiral. It is defined by an hourglass
    coordinate on the wire_frame of the peice.

    Arguments:
        coordinates
    """

    def __init__(self):
        self._coordinates = coordinates


class Pivot(object):
    pass


class Spiral(object):

    def __init__(self, rotation=1, positive=True):
        self._rotation = rotation
        self._positive = positive

    @property
    def rotation(self):
        return self._rotation

    @property
    def positive(self):
        return self._positive


class SquareSpiral(Spiral):
    pass


class
