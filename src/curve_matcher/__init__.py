__version__ = "0.2.0"

from .geometry import (
    Curve,
    Point,
    curve_length,
    extend_point_on_line,
    point_distance,
    rebalance_curve,
    rotate_curve,
    subdivide_curve,
)
from .procrustes_analysis import (
    find_procrustes_rotation_angle,
    procrustes_normalize_curve,
    procrustes_normalize_rotation,
)
from .shape_similarity import shape_similarity

__all__ = [
    "Curve",
    "Point",
    "extend_point_on_line",
    "rebalance_curve",
    "rotate_curve",
    "subdivide_curve",
    "curve_length",
    "point_distance",
    "find_procrustes_rotation_angle",
    "procrustes_normalize_curve",
    "procrustes_normalize_rotation",
    "shape_similarity",
]
