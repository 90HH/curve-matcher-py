import pytest
from curve_matcher.frechet_distance import frechet_distance
from curve_matcher.geometry import Point, rebalance_curve, subdivide_curve

# describe('frechetDist', () => {
#   it('is 0 if the curves are the same', () => {
#     const curve1 = [{ x: 0, y: 0 }, { x: 4, y: 4 }];
#     const curve2 = [{ x: 0, y: 0 }, { x: 4, y: 4 }];

#     expect(frechetDistance(curve1, curve2)).toBe(0);
#     expect(frechetDistance(curve2, curve1)).toBe(0);
#   });


def test_frechet_distance_is_0_if_the_curves_are_the_same():
    curve1 = [Point(0, 0), Point(4, 4)]
    curve2 = [Point(0, 0), Point(4, 4)]
    assert frechet_distance(curve1, curve2) == 0
    assert frechet_distance(curve2, curve1) == 0


#   it('less than then max length of any segment if curves are identical', () => {
#     const curve1 = [{ x: 0, y: 0 }, { x: 2, y: 2 }, { x: 4, y: 4 }];
#     const curve2 = [{ x: 0, y: 0 }, { x: 4, y: 4 }];

#     expect(
#       frechetDistance(
#         subdivideCurve(curve1, { maxLen: 0.5 }),
#         subdivideCurve(curve2, { maxLen: 0.5 })
#       )
#     ).toBeLessThan(0.5);
#     expect(
#       frechetDistance(
#         subdivideCurve(curve1, { maxLen: 0.1 }),
#         subdivideCurve(curve2, { maxLen: 0.1 })
#       )
#     ).toBeLessThan(0.1);
#     expect(
#       frechetDistance(
#         subdivideCurve(curve1, { maxLen: 0.01 }),
#         subdivideCurve(curve2, { maxLen: 0.01 })
#       )
#     ).toBeLessThan(0.01);
#   });


def test_frechet_distance_is_less_than_then_max_length_of_any_segment_if_curves_are_identical():
    curve1 = [Point(0, 0), Point(2, 2), Point(4, 4)]
    curve2 = [Point(0, 0), Point(4, 4)]
    assert (
        frechet_distance(
            subdivide_curve(curve1, max_len=0.5), subdivide_curve(curve2, max_len=0.5)
        )
        < 0.5
    )
    assert (
        frechet_distance(
            subdivide_curve(curve1, max_len=0.1), subdivide_curve(curve2, max_len=0.1)
        )
        < 0.1
    )
    assert (
        frechet_distance(
            subdivide_curve(curve1, max_len=0.01), subdivide_curve(curve2, max_len=0.01)
        )
        < 0.01
    )

    #   it('will be the dist of the starting points if those are the only difference', () => {
    #     const curve1 = [{ x: 1, y: 0 }, { x: 4, y: 4 }];
    #     const curve2 = [{ x: 0, y: 0 }, { x: 4, y: 4 }];

    #     expect(frechetDistance(curve1, curve2)).toBe(1);
    #     expect(frechetDistance(curve2, curve1)).toBe(1);
    #   });


def test_frechet_distance_will_be_the_dist_of_the_starting_points_if_those_are_the_only_difference():
    curve1 = [Point(1, 0), Point(4, 4)]
    curve2 = [Point(0, 0), Point(4, 4)]
    assert frechet_distance(curve1, curve2) == 1
    assert frechet_distance(curve2, curve1) == 1


#   it('gives correct results 1', () => {
#     const curve1 = [
#       { x: 1, y: 0 },
#       { x: 2.4, y: 43 },
#       { x: -1, y: 4.3 },
#       { x: 4, y: 4 }
#     ];
#     const curve2 = [{ x: 0, y: 0 }, { x: 14, y: 2.4 }, { x: 4, y: 4 }];

#     expect(frechetDistance(curve1, curve2)).toBeCloseTo(39.0328);
#   });


def test_frechet_distance_gives_correct_results_1():
    curve1 = [Point(1, 0), Point(2.4, 43), Point(-1, 4.3), Point(4, 4)]
    curve2 = [Point(0, 0), Point(14, 2.4), Point(4, 4)]
    assert frechet_distance(curve1, curve2) == pytest.approx(39.0328)


#   it('gives correct results 2', () => {
#     const curve1 = [
#       { x: 63.44852183813086, y: 24.420192387119634 },
#       { x: 19.472881275654252, y: 77.306125067647 },
#       { x: 22.0150089075698, y: 5.115699052924483 },
#       { x: 90.85925658487311, y: 80.37914225209231 },
#       { x: 96.81784894898642, y: 81.33960258698878 },
#       { x: 75.45756084113779, y: 96.87017085629488 },
#       { x: 87.77706429291412, y: 15.70163068744641 },
#       { x: 37.36893642596093, y: 44.86136460914203 },
#       { x: 37.35720453846581, y: 90.65479959420186 },
#       { x: 41.28185352889147, y: 34.02195976325355 },
#       { x: 27.65820587389076, y: 12.382281496757997 },
#       { x: 42.43674529129338, y: 33.38959395979349 },
#       { x: 3.377463737709774, y: 52.387593489371966 },
#       { x: 50.93481600582428, y: 16.868378936261696 },
#       { x: 68.46675900966153, y: 52.04265123799294 },
#       { x: 1.9235036598383326, y: 55.87935516876048 },
#       { x: 28.02334783421687, y: 98.08317663407114 },
#       { x: 53.74539146366855, y: 33.27918237496243 },
#       { x: 49.39670128874036, y: 47.59663728140997 },
#       { x: 47.51990428391566, y: 11.23339071630216 },
#       { x: 53.31256301680558, y: 55.4279696833061 },
#       { x: 38.797168750480026, y: 26.172634107810833 },
#       { x: 45.604650160570515, y: 71.69212699940685 },
#       { x: 36.83931368726911, y: 38.74324014933978 },
#       { x: 68.76987877419623, y: 1.2518741233677577 },
#       { x: 91.27606575268427, y: 96.2141050404784 },
#       { x: 24.407614843135406, y: 76.20115332073458 },
#       { x: 8.764170623754097, y: 37.003392529458104 },
#       { x: 52.97112238152346, y: 9.76631343977752 },
#       { x: 88.85357966283867, y: 60.767524033054144 }
#     ];
#     const curve2 = [{ x: 0, y: 0 }, { x: 14, y: 2.4 }, { x: 4, y: 4 }];

#     expect(frechetDistance(curve1, curve2)).toBeCloseTo(121.5429);
#   });


def test_frechet_distance_gives_correct_results_2():
    curve1 = [
        Point(63.44852183813086, 24.420192387119634),
        Point(19.472881275654252, 77.306125067647),
        Point(22.0150089075698, 5.115699052924483),
        Point(90.85925658487311, 80.37914225209231),
        Point(96.81784894898642, 81.33960258698878),
        Point(75.45756084113779, 96.87017085629488),
        Point(87.77706429291412, 15.70163068744641),
        Point(37.36893642596093, 44.86136460914203),
        Point(37.35720453846581, 90.65479959420186),
        Point(41.28185352889147, 34.02195976325355),
        Point(27.65820587389076, 12.382281496757997),
        Point(42.43674529129338, 33.38959395979349),
        Point(3.377463737709774, 52.387593489371966),
        Point(50.93481600582428, 16.868378936261696),
        Point(68.46675900966153, 52.04265123799294),
        Point(1.9235036598383326, 55.87935516876048),
        Point(28.02334783421687, 98.08317663407114),
        Point(53.74539146366855, 33.27918237496243),
        Point(49.39670128874036, 47.59663728140997),
        Point(47.51990428391566, 11.23339071630216),
        Point(53.31256301680558, 55.4279696833061),
        Point(38.797168750480026, 26.172634107810833),
        Point(45.604650160570515, 71.69212699940685),
        Point(36.83931368726911, 38.74324014933978),
        Point(68.76987877419623, 1.2518741233677577),
        Point(91.27606575268427, 96.2141050404784),
        Point(24.407614843135406, 76.20115332073458),
        Point(8.764170623754097, 37.003392529458104),
        Point(52.97112238152346, 9.76631343977752),
        Point(88.85357966283867, 60.767524033054144),
    ]
    curve2 = [Point(0, 0), Point(14, 2.4), Point(4, 4)]
    assert frechet_distance(curve1, curve2) == pytest.approx(121.5429)


#   it("doesn't overflow the node stack if the curves are very long", () => {
#     const curve1 = rebalanceCurve([{ x: 1, y: 0 }, { x: 4, y: 4 }], {
#       numPoints: 5000
#     });
#     const curve2 = rebalanceCurve([{ x: 0, y: 0 }, { x: 4, y: 4 }], {
#       numPoints: 5000
#     });

#     expect(frechetDistance(curve1, curve2)).toBe(1);
#   });
# });


def test_frechet_distance_does_not_overflow_the_node_stack_if_the_curves_are_very_long():
    curve1 = rebalance_curve([Point(1, 0), Point(4, 4)], num_points=5000)
    curve2 = rebalance_curve([Point(0, 0), Point(4, 4)], num_points=5000)
    assert frechet_distance(curve1, curve2) == 1
