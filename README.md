# Curve Matcher Python

[![ci](https://img.shields.io/github/actions/workflow/status/90HH/curve-matcher-py/ci.yaml?branch=main)](https://github.com/90HH/curve-matcher-py)
[![PyPI](https://img.shields.io/pypi/v/curve-matcher?color=blue)](https://pypi.org/project/curve-matcher/)
[![license](https://badgen.net/static/license/MIT/blue)](https://opensource.org/licenses/MIT)

A Python library for doing curve matching with Fréchet distance and Procrustes analysis, ported from the [Javascript curve-matcher library](https://github.com/90HH/curve-matcher-py).

## Installation

Curve matcher can be installed via pip:

```
pip install curve-matcher
```

## Getting started

The core of `curve-matcher` is a function called `shape_similarity` which estimates how similar the shapes of 2 curves are to each other, returning a value between `0` and `1`.

![shape_similarity example curves](http://misc-cdn-assets.s3-us-west-2.amazonaws.com/shape_similarity.png)

Curves are defined as lists of points of `x` and `y` like below:

```python
from curve_matcher import Point
curve = [Point(x=2, y=1.5), Point(x=4, y=3), ... ]
```

calculating similarity between 2 curves is as simple as calling:

```python
from curve_matcher import shape_similarity

# 1 means identical shape, 0 means very different shapes
similarity = shape_similarity(curve1, curve2)
```

`shape_similarity` automatically adjusts for rotation, scale, and translation differences between so it doesn't matter if the curves are different sizes or in different locations on the screen - as long as they have the same shape the similarity score will be close to `1`.

You can further customize the accuracy of the `shape_similarity` function by changing `estimation_points` (default 50) and `rotations` (default 10). Increasing these will improve accuracy, but the function will take longer to run.

```python
# higher accuracy, but slower
shape_similarity(curve1, curve2, estimation_points=200, rotations=30)

# lower accuracy, but faster
shape_similarity(curve1, curve2, estimation_points=10, rotations=0)
```

You can also restrict the range of rotations that are checked using the `restrict_rotation_angle` option. This option means the shape_similarity function will only check rotations within +- `restrict_rotation_angle` radians. If you'd like to disable rotation correction entirely, you can set `check_rotations=False`. These are shown below:

```python
# Only check rotations between -0.1 π to 0.1 π
shape_similarity(curve1, curve2, restrict_rotation_angle=0.1 * math.pi)

# disable rotation correction entirely
shape_similarity(curve1, curve2, check_rotations=False)
```

## How it works

Internally, `shape_similarity` works by first normalizing the curves using [Procrustes analysis](https:#en.wikipedia.org/wiki/Procrustes_analysis) and then calculating [Fréchet distance](https:#en.wikipedia.org/wiki/Fr%C3%A9chet_distance) between the curves.

Procrustes analysis attempts to translate both the curves to the origin and adjust their scale so they're the same size. Then, it rotates the curves so their rotations are as close as possible.

In practice, Procrustes analysis has 2 issues which curve-matcher works to address.
First, it's very dependent on how the points of the curve are spaced apart from each other. To account for this, `shape_similarity` first redraws each curve using 50 (by default) points equally spaced out along the length of the curve. In addition, Procrustes analysis sometimes doesn't choose the best rotation if curves are not that similar to each other, so `shape_similarity` also tries 10 (by default) equally spaced rotations to make sure it picks the best possible rotation normalization. You can adjust these parameters via the `estimation_points` and `rotations` options to `shape_similarity`.

If you'd like to implement your own version of `shape_similarity` there's a number of helper methods that are exported by `curve-matcher` which you can use as well, discussed below:

## Fréchet distance

Curve matcher includes an implemention of a discreet Fréchet distance algorithm from the paper [Computing Discrete Fréchet Distance](http:#www.kr.tuwien.ac.at/staff/eiter/et-archive/cdtr9464.pdf). You can use this function by passing in 2 curves, as below:

```python
from curve_matcher import frechet_distance

dist = frechet_distance(curve1, curve2)
```

As with `shape_similarity`, curves are in the format `[Point(x=2, y=1.5), Point(x=4, y=3), ... ]`.

A caveat of discreet Fréchet distance is that the calculation is only as accurate as the length of the line segments of the curves. That means, if curves have long distances between each of the points in the curve, or if there's not many points in the curve, the calculation may be inaccurate. To help alleviate this, Curve matcher provides a helper method called `subdivide_curve` which takes a curve and splits up line segments in the curve to improve the accuracy of the Fréchet distance calculation. This can be used as below:

```python
from curve_matcher import frechet_distance, subdivide_curve

# subdivide the curves so each segment is at most length 0.5
dividedCurve1 = subdivide_curve(curve1, maxLen=0.5)
dividedCurve2 = subdivide_curve(curve2, maxLen=0.5)

# now, the frechet distance is guaranteed to be at most off by 0.5
dist = frechet_distance(dividedCurve1, dividedCurve2)
```

## Procrustes analysis

Curve matcher also exports a few methods to help with Procrustes analysis. However, before running these it's recommended that curves be rebalanced so that the points of the curve are all equally spaced along its length. This can be done with a function called `rebalance_curve` as below:

```python
from curve_matcher import rebalance_curve

# redraw the curve using 50 equally spaced points
balanced_curve = rebalance_curve(curve, numPoints=50)
```

Then, to normalize scale and translation, pass the curve into `procrustes_normalize_curve` as below:

```python
from curve_matcher import procrustes_normalize_curve, rebalance_curve

balanced_curve = rebalance_curve(curve)
scaledAndTranslatedCurve = procrustes_normalize_curve(balanced_curve)
```

There's also a function provided called `procrustes_normalize_rotation` to help normalize rotation using Procrustes analysis. It should be noted that this may give odd results if the 2 curves don't have a relatively similar shape to each other. Make sure that the curves are already rebalanced and have scale and translation normalized before using this function. This function can be used as below:

```python
from curve_matcher import (
  procrustes_normalize_curve,
  procrustes_normalize_rotation,
  rebalance_curve,
)

# first rebalance and normalize scale and translation of the curves
normalizedCurve1 = procrustes_normalize_curve(rebalance_curve(curve1))
normalizedCurve2 = procrustes_normalize_curve(rebalance_curve(curve2))

# rotate normalizedCurve1 to match normalizedCurve2
rotatedCurve1 = procrustes_normalize_rotation(
  normalizedCurve1,
  normalizedCurve2
)
```

You can read more about these algorithms here: https://en.wikipedia.org/wiki/Procrustes_analysis

## License

Curve matcher is released under a [MIT License](https://opensource.org/licenses/MIT).

## Contributing

Contributions are welcome! These steps will guide you through contributing to this project:

- Fork the repo
- Clone it and install dependencies
  ```
  git clone https://github.com/90HH/curve-matcher-py
  pdm install
  ```

Make and commit your changes. This project uses [PDM](https://pdm-project.org/latest/) for dependency management, [Ruff](https://docs.astral.sh/ruff/) for linting / formatting, and [Pyright](https://github.com/microsoft/pyright) for type checking. Make sure any changes pass linting and type-checking by running `pdm run pyright` and `pdm run ruff .` before committing.

Finally send a [GitHub Pull Request](https://github.com/90HH/curve-matcher-py/compare?expand=1) with a clear list of what you've done. Make sure all of your commits are atomic (one feature per commit). Please add tests for any features that you add or change.

## Sources

This library is a port of the [Javascript curve-matcher library](https://github.com/chanind/curve-matcher), which was extracted from stroke matching code in [Hanzi Writer](https://chanind.github.io/hanzi-writer).

Procrustes analysis algorithms are from https://en.wikipedia.org/wiki/Procrustes_analysis

Discrete Fréchet distance algorithm is from [Computing Discrete Fréchet Distance](http://www.kr.tuwien.ac.at/staff/eiter/et-archive/cdtr9464.pdf)

**Happy curve matching!**
