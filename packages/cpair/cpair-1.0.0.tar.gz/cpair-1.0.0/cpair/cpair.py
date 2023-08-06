#
# Copyright (C) 2021 Kian Cross
#

"""
Implementation of the closest pairs algorithm found here:
https://www.cs.umd.edu/~samir/grant/cp.pdf

Has O(n) expected running time.
"""

from typing import List, Tuple, Dict

import math
import random

from .point import Point

MeshKeyType = Tuple[int, int]
MeshType = Dict[MeshKeyType, List[Point]]

Infinity = float("inf")


def get_key(point: Point, interval: float) -> MeshKeyType:
    """
    Uses an interval to get the key for a particular point to
    be used in a dictionary.

    Points within the same interval are guaranteed to get the
    same key.

    Args:
        point: The point to get the key for.

        interval: The mesh interval being used.

    Returns:
        The key.
    """
    return (math.floor(point.x / interval), math.floor(point.y / interval))


def get_closest_to_point(root_point: Point, points: List[Point]) -> float:
    """
    Gets the closest distance to a point from a list of points.

    Args:
        root_point: The point to check all other distances to.

        points: The list of points to compare with the root_point.

    Returns:
        The closest distance between
    """
    min_distance = Infinity

    for point in points:
        if root_point is point:
            continue

        distance = root_point.distance(point)

        min_distance = min(distance, min_distance)

    return min_distance


def get_mesh(points: List[Point], interval: float) -> MeshType:
    """
    Gets the mesh for a particular set of points using the
    given interval size.

    Args:
        points: The set of points to put into the mesh.

        interval: The interval size to use.

    Returns:
        The mesh.
    """
    mesh: MeshType = {}

    for point in points:
        key = get_key(point, interval)
        if key not in mesh:
            mesh[key] = []

        mesh[key].append(point)

    return mesh


def get_neighbourhood(mesh: MeshType, point: Point, interval: float) -> List[Point]:
    """
    Gets the neighbourhood for a particular point in a mesh.

    The neighbourhood is defined as points in the surrounding 8
    cells around the point.

    Args:
        mesh: The mesh.

        point: The point for which the neighbourhood is to be found.

    Returns:
        The list of points in the given point's neighbourhood.
    """

    neighbourhood = []
    point_key = get_key(point, interval)

    for x_delta in range(-1, 2):
        for y_delta in range(-1, 2):
            neighbour_key = (point_key[0] + x_delta, point_key[1] + y_delta)

            if neighbour_key in mesh:
                neighbourhood += mesh[neighbour_key]

    neighbourhood.remove(point)

    return neighbourhood


def get_minimum_approximation(points: List[Point]) -> float:
    """
    Gets an approximated minimum distance for the closest points in
    a list of points.

    Args:
        points: The points in which to find the approximated minimum.

    Returns:
        The approximated minimum distance between the two closest points
        in the list.
    """

    point = random.choice(points)
    min_distance = get_closest_to_point(point, points)

    # If the minimum distance is 0, then we had a duplicate point.
    # We can't get a distance smaller than 0, so stop here.
    if min_distance == 0:
        return 0

    interval = min_distance / 3
    mesh = get_mesh(points, interval)

    # Create a new array for filtered points, rather than removing
    # points from the current array (which takes O(n)).
    filtered_points = []

    for bucket in mesh.values():
        if len(bucket) == 1:
            point = bucket[0]
            neighbourhood = get_neighbourhood(mesh, point, interval)

            if len(neighbourhood) > 0:
                filtered_points.append(point)

    if len(filtered_points) == 0:
        return min_distance

    return get_minimum_approximation(filtered_points)


def closest_pair(points: List[Point]) -> float:
    """
    Returns the distance between the two closest points.

    Args:
        points: The points in which to find the closest pair.

    Returns:
        The distance between the closest pair of points.
    """

    approximated_minimum = get_minimum_approximation(points[:])

    # If the minimum distance is 0, then we had a duplicate point.
    # We can't get a distance smaller than 0, so stop here.
    if approximated_minimum == 0:
        return 0

    mesh = get_mesh(points, approximated_minimum)

    min_distance = Infinity

    for point in points:
        neighbourhood = get_neighbourhood(mesh, point, approximated_minimum)
        closest_distance = get_closest_to_point(point, neighbourhood)

        min_distance = min(min_distance, closest_distance)

    return min_distance
