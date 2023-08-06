#
# Copyright (C) 2021 Kian Cross
#

from typing import Any

import math


class Point:
    """
    Class representing a point on a plane.
    """

    def __init__(self, x: float, y: float):
        """
        Constructs a 2d point.

        Args:
            x: The x-coordinate of the point.

            y: The y-coordinate of the point.
        """
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """
        Returns a string representation of the point.
        """
        return "(x=%lf, y=%lf)" % (self.x, self.y)

    def __sub__(self, other: Any) -> "Point":
        """
        Subtract another point from this point.

        Args:
            other: The point to be subtracted from this
                   point.

        Returns:
            The resultant point.

        Raises:
            ValueError: If the other operand is not a point.
        """

        if not isinstance(other, Point):
            raise ValueError("Both operands must be points")

        x_delta = self.x - other.x
        y_delta = self.y - other.y

        return Point(x_delta, y_delta)

    def __eq__(self, other: Any) -> bool:
        """
        Check if this point equals another point.

        Args:
            other: The point to check equality with.

        Returns:
            Whether the points are equal.

        Raises:
            ValueError: If the other operand is not a point.
        """

        if not isinstance(other, Point):
            raise ValueError("Both operands must be points")

        return self.x == other.x and self.y == other.y

    def __abs__(self) -> float:
        """
        Calculates the euclidean distance of a point from the
        origin.

        Returns:
            The euclidean distance of the point from the origin.
        """
        return math.sqrt((self.x ** 2) + (self.y ** 2))

    def distance(self, other: "Point") -> float:
        """
        Calculates the distance between this point and another
        point.

        Args:
            other: The other point to calculate the distance from.

        Returns:
            The distance between this point and another point.
        """
        return abs(self - other)
