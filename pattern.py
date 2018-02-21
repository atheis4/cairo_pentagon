"""
Should I have a binary mode and a cartesian mode?

Binary mode would track 8 data points:
    r_inc: 0 for no increase, 1 for increase
    r_dec: 0 for no decrease, 1 for decrease
    c_inc: 0 for no increase, 1 for increase
    c_dec: 0 for no decrease, 1 for decrease
    r_h: 0 for no row height, 1 for row height
    c_h: 0 for no column height, 1 for column height
    t1: 0 for tile pattern A, 1 for tile pattern B
    t2: 0 for tile pattern A, 1 for tile pattern B

Cartesian mode would simplify the points to:
    delta_r: -1, 0, or 1 for the change in the row index value
    delta_c: -1, 0, or 1 for the change in the column index value
    dimension: 0 for column height but no row height, 1 for row height and no
        column height
    t1: 0 for A, 1 for B
"""


import numpy as np


class Movement(object):
    """.
    """

    def __init__(self, is_positive, is_negative, dimension):
        self.is_positive = is_positive
        self.is_negative = is_negative
        self.dimension = dimension


class Origin(object):
    """
    The origin object begins the spiral. It is defined by an hourglass
    coordinate on the wire_frame of the peice.

    Arguments:
        row_index (int): row position on WireFrame.frame
        col_index (int): column position on WireFrame.frame
        dimension (int): which
        init_tile (int):
    """

    def __init__(self,
                 row_index=0,
                 col_index=0,
                 dimension=0
                 init_tile=0):
        self._row_index = row_index
        self._col_index = col_index
        self._dimension = dimension
        self._init_tile = init_tile


class SpiralArm(object):
    """
    For positive v negative space: consider everything to be positive space
    during rendering... Negative space will represent tiles without color,
    carved into an entire TileFrame of a single color.

    Arguments:
        rotation (String): 'cw' or 'ccw' (default 'cw')
        space (String): 'pos' or 'neg' (default 'pos')
    """

    def __init__(self, rotation='cw', space='pos', origin=None):
        self._rotation = rotation
        self._space = space
        self._origin = origin

    @property
    def rotation(self):
        return self._rotation

    @property
    def space(self):
        return self._space

    def run(self):
        raise NotImplementedError(
            "The run method cannot be run on the base class: SpiralArm")


class SquareSpiralArm(Spiral):
    """
    The origin is point 0. A square spiral arm is the most basic meta pattern
    applied to the WireFrame.

    A movement map tracks which type of incrementing and decrementing we need
    to apply to the current piece's coordinates in order to advance the
    pattern.
    """

    def __init__(self, rotation='cw', space='pos', origin=None):
        super().__init__(rotation, space, origin)
        self.current_movement = self.movement_map[0]
        self.pivot_total = 0

    @classmethod
    def negative_row_positive_col(cls):
        """
        Decrement the row by one or zero.
        Increment the column by one or zero.
        """
        delta = np.array([[0, 1], [1, 0]], [[0, 0], [0, 0]])

    @classmethod
    def positive_row_positive_col(cls):
        """
        Increment the row by one or zero.
        Increment the column by one or zero.
        """
        delta = np.array([[0, 0], [1, 0]], [[1, 0], [0, 0]])

    @classmethod
    def negative_row_negative_col(cls):
        """
        Decrement the row by one or zero.
        Decrement the column by one or zero.
        """
        delta = np.array([[0, 1], [0, 0]], [[0, 0], [0, 1]])

    @classmethod
    def positive_row_negative_col(cls):
        """
        Increment the row by one or zero.
        Decrement the column by one or zero.
        """
        delta = np.array([[0, 0], [0, 0]], [[0, 1], [1, 0]])

    def movement_map(self):
        """
        Should be a Queue that rotates by adding the current movement to the
        end of the Queue while progressing to the next step...

        This way, the only difference between clockwise and counterclockwise is
        to advance to the next element or the last element.
        """
        if self.rotation == 'cw':
            return [self.negative_row_positive_col,
                    self.positive_row_positive_col,
                    self.positive_row_negative_col,
                    self.negative_row_negative_col]
        else:
            return [self.negative_row_negative_col,
                    self.positive_row_negative_col,
                    self.positive_row_positive_col,
                    self.negative_row_positive_col]

    def pivot(self):
        """
        Counts the pivots and tells the pattern when to advance to the next
        set of movements in the movement map.
        """
        self.pivot += 1
        self.current_movement = self.movement_map[self.current_movement + 1]

    def run(self, duration=400):
        """
        The core algorithm.

        Combines the incrementing with tracking pivoting and detailing which
        type of motion is necessary to continue the pattern.
        """
        for i in range(1, duration):
            is_pivot = np.sqrt(i) == int(np.sqrt(i))
            if is_pivot:
                self.pivot()
