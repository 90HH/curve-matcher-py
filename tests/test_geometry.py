from curve_matcher.geometry import (
    Point,
    extend_point_on_line,
    rebalance_curve,
    subdivide_curve,
)


def test_extend_point_on_line_returns_point_distance_away_from_end_point():
    p1 = Point(0, 0)
    p2 = Point(8, 6)
    assert extend_point_on_line(p1, p2, 5) == Point(12, 9)


def test_extend_point_on_line_works_with_negative_distances():
    p1 = Point(0, 0)
    p2 = Point(8, 6)
    assert extend_point_on_line(p1, p2, -5) == Point(4, 3)


def test_extend_point_on_line_works_when_p2_is_before_p1_in_the_line():
    p1 = Point(12, 9)
    p2 = Point(8, 6)
    assert extend_point_on_line(p1, p2, 10) == Point(0, 0)


def test_extend_point_on_line_works_with_vertical_lines():
    p1 = Point(2, 4)
    p2 = Point(2, 6)
    assert extend_point_on_line(p1, p2, 7) == Point(2, 13)


def test_extend_point_on_line_works_with_vertical_lines_where_p2_is_above_p1():
    p1 = Point(2, 6)
    p2 = Point(2, 4)
    assert extend_point_on_line(p1, p2, 7) == Point(2, -3)


def test_subdivide_curve_leave_the_curve_the_same_if_segment_lengths_are_less_than_maxLen_apart():
    curve = [Point(0, 0), Point(4, 4)]
    assert subdivide_curve(curve, max_len=10) == [Point(0, 0), Point(4, 4)]


def test_subdivide_curve_breaks_up_segments_so_that_each_segment_is_less_than_maxLen_length():
    curve = [Point(0, 0), Point(4, 4), Point(0, 8)]
    assert subdivide_curve(curve, max_len=2**0.5) == [
        Point(0, 0),
        Point(1, 1),
        Point(2, 2),
        Point(3, 3),
        Point(4, 4),
        Point(3, 5),
        Point(2, 6),
        Point(1, 7),
        Point(0, 8),
    ]


def test_subdivide_curve_uses_maxLen_of_0_05_by_default():
    curve = [Point(0, 0), Point(0, 0.1)]
    assert subdivide_curve(curve) == [Point(0, 0), Point(0, 0.05), Point(0, 0.1)]


def test_rebalance_curve_divides_a_curve_into_equally_spaced_segments():
    curve1 = [Point(0, 0), Point(4, 6)]
    assert rebalance_curve(curve1, num_points=3) == [
        Point(0, 0),
        Point(2, 3),
        Point(4, 6),
    ]
    curve2 = [Point(0, 0), Point(9, 12), Point(0, 24)]
    print(rebalance_curve(curve2, num_points=4))
    assert rebalance_curve(curve2, num_points=4) == [
        Point(0, 0),
        Point(6, 8),
        Point(6, 16),
        Point(0, 24),
    ]
