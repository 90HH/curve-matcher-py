import math

from curve_matcher.geometry import Curve, Point, rebalance_curve, rotate_curve, subtract


def procrustes_normalize_curve(
    curve: Curve,
    rebalance: bool = True,
    estimation_points: int = 50,
) -> Curve:
    """
    Translate and scale curve by Procrustes Analysis
    Optionally runs rebalance_curve first (default True)
    from https://en.wikipedia.org/wiki/Procrustes_analysis
    """
    if rebalance:
        curve = rebalance_curve(curve, num_points=estimation_points)
    mean_x = sum(point.x for point in curve) / len(curve)
    mean_y = sum(point.y for point in curve) / len(curve)
    mean = Point(mean_x, mean_y)
    translated_curve = [subtract(point, mean) for point in curve]
    scale = math.sqrt(
        sum(point.x**2 + point.y**2 for point in translated_curve)
        / len(translated_curve)
    )
    return [Point(point.x / scale, point.y / scale) for point in translated_curve]


def find_procrustes_rotation_angle(
    curve: Curve,
    relative_curve: Curve,
) -> float:
    """
    Find the angle to rotate `curve` to match the rotation of `relativeCurve` using procrustes analysis
    from https://en.wikipedia.org/wiki/Procrustes_analysis

    `curve` and `relativeCurve` must have the same number of points
    `curve` and `relativeCurve` should both be run through procrustes_normalize_curve first
    """
    if len(curve) != len(relative_curve):
        raise ValueError("curve and relativeCurve must have the same length")
    numerator = sum(
        point.y * relative_point.x - point.x * relative_point.y
        for point, relative_point in zip(curve, relative_curve)
    )
    denominator = sum(
        point.x * relative_point.x + point.y * relative_point.y
        for point, relative_point in zip(curve, relative_curve)
    )
    return math.atan2(numerator, denominator)


def procrustes_normalize_rotation(
    curve: Curve,
    relative_curve: Curve,
) -> Curve:
    """
    Rotate `curve` to match the rotation of `relativeCurve` using procrustes analysis
    from https://en.wikipedia.org/wiki/Procrustes_analysis

    `curve` and `relativeCurve` must have the same number of points
    `curve` and `relativeCurve` should both be run through procrustes_normalize_curve first
    """
    angle = find_procrustes_rotation_angle(curve, relative_curve)
    return rotate_curve(curve, angle)
