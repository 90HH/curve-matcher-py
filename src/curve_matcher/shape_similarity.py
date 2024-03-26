import math

from curve_matcher.frechet_distance import frechet_distance
from curve_matcher.geometry import Curve, curve_length, rotate_curve
from curve_matcher.procrustes_analysis import (
    find_procrustes_rotation_angle,
    procrustes_normalize_curve,
)


def shape_similarity(
    curve1: Curve,
    curve2: Curve,
    estimation_points: int = 50,
    rotations: int = 10,
    restrict_rotation_angle: float = math.pi,
    check_rotations: bool = True,
) -> float:
    if abs(restrict_rotation_angle) > math.pi:
        raise ValueError("restrict_rotation_angle cannot be larger than PI")
    normalized_curve1 = procrustes_normalize_curve(
        curve1, estimation_points=estimation_points
    )
    normalized_curve2 = procrustes_normalize_curve(
        curve2, estimation_points=estimation_points
    )
    geo_avg_curve_len = math.sqrt(
        curve_length(normalized_curve1) * curve_length(normalized_curve2)
    )
    thetas_to_check = [0.0]
    if check_rotations:
        procrustes_theta = find_procrustes_rotation_angle(
            normalized_curve1, normalized_curve2
        )
        if procrustes_theta > math.pi:
            procrustes_theta = procrustes_theta - 2 * math.pi
        if procrustes_theta != 0 and abs(procrustes_theta) < restrict_rotation_angle:
            thetas_to_check.append(procrustes_theta)
        for i in range(rotations):
            theta = -1 * restrict_rotation_angle + (2 * i * restrict_rotation_angle) / (
                rotations - 1
            )
            if theta != 0 and theta != math.pi:
                thetas_to_check.append(theta)
    min_frechet_dist = float("inf")
    for theta in thetas_to_check:
        rotated_curve1 = rotate_curve(normalized_curve1, theta)
        dist = frechet_distance(rotated_curve1, normalized_curve2)
        if dist < min_frechet_dist:
            min_frechet_dist = dist
    return max(1 - min_frechet_dist / (geo_avg_curve_len / math.sqrt(2)), 0)
