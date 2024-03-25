import math
from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float


Curve = list[Point]


def subtract(v1: Point, v2: Point) -> Point:
    return Point(v1.x - v2.x, v1.y - v2.y)


def magnitude(v: Point) -> float:
    return (v.x**2 + v.y**2) ** 0.5


def point_distance(point1: Point, point2: Point) -> float:
    """
    Calculate the distance between 2 points
    """
    return magnitude(subtract(point1, point2))


def curve_length(points: Curve) -> float:
    """
    Calculate the length of the curve
    """
    return sum(point_distance(p1, p2) for p1, p2 in zip(points, points[1:]))


def extend_point_on_line(p1: Point, p2: Point, dist: float) -> Point:
    """
    return a new point, p3, which is on the same line as p1 and p2, but <dist> away from p2
    p1, p2, p3 will always lie on the line in that order (as long as dist is positive)
    """
    vect = subtract(p2, p1)
    norm = dist / magnitude(vect)
    return Point(p2.x + norm * vect.x, p2.y + norm * vect.y)


def subdivide_curve(curve: Curve, max_len: float = 0.05) -> Curve:
    """
    Break up long segments in the curve into smaller segments of len max_len or smaller
    """
    new_curve = curve[:1]
    for point in curve[1:]:
        prev_point = new_curve[-1]
        seg_len = point_distance(point, prev_point)
        if seg_len > max_len:
            num_new_points = int(seg_len / max_len)
            new_seg_len = seg_len / num_new_points
            for i in range(num_new_points):
                new_curve.append(
                    extend_point_on_line(point, prev_point, -1 * new_seg_len * (i + 1))
                )
        else:
            new_curve.append(point)
    return new_curve


def rebalance_curve(curve: Curve, num_points: int = 50) -> Curve:
    """
    Redraw the curve using `num_points` points equally spaced along the length of the curve
    This may result in a slightly different shape than the original if `num_points` is low
    """
    curve_len = curve_length(curve)
    segment_len = curve_len / (num_points - 1)
    outline_points = [curve[0]]
    end_point = curve[-1]
    remaining_curve_points = curve[1:]
    for _ in range(num_points - 2):
        last_point = outline_points[-1]
        remaining_dist = segment_len
        outline_point_found = False
        while not outline_point_found:
            next_point_dist = point_distance(last_point, remaining_curve_points[0])
            if next_point_dist < remaining_dist:
                remaining_dist -= next_point_dist
                last_point = remaining_curve_points.pop(0)
            else:
                next_point = extend_point_on_line(
                    last_point,
                    remaining_curve_points[0],
                    remaining_dist - next_point_dist,
                )
                outline_points.append(next_point)
                outline_point_found = True
    outline_points.append(end_point)
    return outline_points


def rotate_curve(curve: Curve, theta: float) -> Curve:
    """
    Rotate the curve around the origin
    """
    return [
        Point(
            x=math.cos(-1 * theta) * point.x - math.sin(-1 * theta) * point.y,
            y=math.sin(-1 * theta) * point.x + math.cos(-1 * theta) * point.y,
        )
        for point in curve
    ]
