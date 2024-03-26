import math
from random import random

import pytest
from curve_matcher.geometry import Curve, Point, rotate_curve
from curve_matcher.shape_similarity import shape_similarity


def translate_scale_and_rotate(
    curve: Curve, translation: float, scale: float, theta: float
) -> Curve:
    return rotate_curve(
        [
            Point(scale * (point.x + translation), scale * (point.y + translation))
            for point in curve
        ],
        theta,
    )


def random_curve(length: int) -> Curve:
    return [Point(random(), random()) for _ in range(length)]


rotations = [math.pi / 3, 1.3 * math.pi, math.pi, -1]
translations = [18, -3, -2000, 90, 1.345]
scales = [0.2, 1.7, 10, 2000]


def test_shape_similarity_returns_1_if_curves_are_identical_no_matter_the_rotation_scale_and_translation_between_the_curves():
    curve = [Point(0, 0), Point(2, 4), Point(18, -3)]
    for theta in rotations:
        for translation in translations:
            for scale in scales:
                new_curve = translate_scale_and_rotate(curve, translation, scale, theta)
                assert shape_similarity(curve, new_curve) == pytest.approx(1)


def test_shape_similarity_allows_restricting_the_rotation_angles_that_are_checked():
    curve = [Point(0, 0), Point(2, 4), Point(18, -3)]
    within_range_rotations = [0, -0.2, -0.3, 0.2, 0.3]
    out_of_range_rotations = [-0.5, 0.5, math.pi]
    for translation in translations:
        for scale in scales:
            for theta in within_range_rotations:
                new_curve = translate_scale_and_rotate(curve, translation, scale, theta)
                assert shape_similarity(
                    curve, new_curve, restrict_rotation_angle=0.3
                ) == pytest.approx(1)
            for theta in out_of_range_rotations:
                new_curve = translate_scale_and_rotate(curve, translation, scale, theta)
                assert (
                    shape_similarity(curve, new_curve, restrict_rotation_angle=0.3)
                    < 0.9
                )


def test_shape_similarity_errors_if_restrict_rotation_angle_is_invalid():
    curve = [Point(0, 0), Point(2, 4)]
    with pytest.raises(ValueError) as e:
        shape_similarity(curve, curve, restrict_rotation_angle=340)
    assert str(e.value) == "restrict_rotation_angle cannot be larger than PI"
    with pytest.raises(ValueError) as e:
        shape_similarity(curve, curve, restrict_rotation_angle=3 * math.pi)
    assert str(e.value) == "restrict_rotation_angle cannot be larger than PI"
    with pytest.raises(ValueError) as e:
        shape_similarity(curve, curve, restrict_rotation_angle=-1.1 * math.pi)
    assert str(e.value) == "restrict_rotation_angle cannot be larger than PI"


def test_shape_similarity_returns_close_to_1_if_curves_have_similar_shapes():
    curve1 = [Point(0, 0), Point(2, 4), Point(18, -3)]
    curve2 = [Point(0.3, -0.2), Point(2.2, 4.5), Point(16, -4)]
    for theta in rotations:
        for translation in translations:
            for scale in scales:
                new_curve2 = translate_scale_and_rotate(
                    curve2, translation, scale, theta
                )
                assert shape_similarity(curve1, new_curve2) > 0.8


def test_shape_similarity_allows_overriding_rotations_and_estimation_points_to_tradeoff_accuracy_and_speed():
    curve1 = [Point(0, 0), Point(2, 4), Point(18, -3)]
    curve2 = [Point(0.3, -0.2), Point(2.2, 4.5), Point(16, -4)]
    for theta in rotations:
        for translation in translations:
            for scale in scales:
                new_curve2 = translate_scale_and_rotate(
                    curve2, translation, scale, theta
                )
                assert (
                    shape_similarity(
                        curve1, new_curve2, rotations=0, estimation_points=10
                    )
                    > 0.8
                )


def test_shape_similarity_returns_low_numbers_for_curves_with_dissimilar_shapes():
    curve1 = [Point(0, 0), Point(2, 4), Point(4, 0), Point(0, 0)]
    curve2 = [Point(0, 0), Point(4, 4)]
    assert shape_similarity(curve1, curve2) < 0.5


def test_shape_similarity_should_be_really_close_to_0_for_very_dissimilar_shapes():
    curve1 = [Point(0, 0), Point(1, 1), Point(0, 0)]
    curve2 = [Point(0, 0), Point(1, 1)]
    assert shape_similarity(curve1, curve2) < 0.25
