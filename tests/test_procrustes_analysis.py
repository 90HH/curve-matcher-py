import math
from math import sqrt

import pytest
from curve_matcher.geometry import Point
from curve_matcher.procrustes_analysis import (
    find_procrustes_rotation_angle,
    procrustes_normalize_curve,
    procrustes_normalize_rotation,
)


def test_procrustes_normalize_curve_normalizes_the_scale_and_translation_of_the_curve():
    curve = [Point(0, 0), Point(4, 4)]
    assert procrustes_normalize_curve(curve, rebalance=False) == [
        pytest.approx(Point(-1 * sqrt(2) / 2, -1 * sqrt(2) / 2)),
        pytest.approx(Point(sqrt(2) / 2, sqrt(2) / 2)),
    ]


def test_procrustes_normalize_curve_rebalances_with_50_points_by_default():
    curve = [Point(0, 0), Point(4, 4)]
    normalized_curve = procrustes_normalize_curve(curve)
    assert len(normalized_curve) == 50


def test_procrustes_normalize_curve_can_be_configured_to_rebalance_with_a_custom_number_of_points():
    curve = [Point(0, 0), Point(4, 4)]
    normalized_curve = procrustes_normalize_curve(curve, estimation_points=3)
    assert normalized_curve == [
        pytest.approx(Point(-1 * sqrt(3) / 2, -1 * sqrt(3) / 2)),
        pytest.approx(Point(0, 0)),
        pytest.approx(Point(sqrt(3) / 2, sqrt(3) / 2)),
    ]


def test_procrustes_normalize_curve_gives_identical_results_for_identical_curves_with_different_numbers_of_points_after_rebalancing():
    curve1 = [Point(0, 0), Point(4, 4)]
    curve2 = [Point(0, 0), Point(3, 3), Point(4, 4)]
    assert procrustes_normalize_curve(curve1) == [
        pytest.approx(point) for point in procrustes_normalize_curve(curve2)
    ]


def test_find_procrustes_rotation_angle_determines_the_optimal_rotation_angle_to_match_2_curves_on_top_of_each_other():
    curve1 = procrustes_normalize_curve([Point(0, 0), Point(1, 0)])
    curve2 = procrustes_normalize_curve([Point(0, 0), Point(0, 1)])
    assert find_procrustes_rotation_angle(curve1, curve2) == pytest.approx(
        (-1 * math.pi) / 2
    )


def test_find_procrustes_rotation_angle_returns_0_if_the_curves_have_the_same_rotation():
    curve1 = [Point(0, 0), Point(1, 1)]
    curve2 = [Point(0, 0), Point(1.5, 1.5)]
    assert find_procrustes_rotation_angle(curve1, curve2) == 0


def test_procrustes_normalize_rotation_rotates_a_normalized_curve_to_match_the_rotation_of_another_normalized_curve():
    curve = procrustes_normalize_curve([Point(0, 0), Point(1, 0)])
    relative_curve = procrustes_normalize_curve([Point(0, 0), Point(0, 1)])
    rotated_curve = procrustes_normalize_rotation(curve, relative_curve)
    assert rotated_curve == [pytest.approx(point) for point in relative_curve]


def test_procrustes_normalize_rotation_throws_an_error_if_the_curves_have_different_numbers_of_points():
    curve1 = [Point(0, 0), Point(1, 1)]
    curve2 = [Point(0, 0), Point(1, 1), Point(1.5, 1.5)]
    with pytest.raises(ValueError):
        procrustes_normalize_rotation(curve1, curve2)
