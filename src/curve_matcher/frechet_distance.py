# import { Curve, pointDistance } from './geometry';
from curve_matcher.geometry import Curve, point_distance

# /**
#  * Discrete Frechet distance between 2 curves
#  * based on http://www.kr.tuwien.ac.at/staff/eiter/et-archive/cdtr9464.pdf
#  * modified to be iterative and have better memory usage
#  */
# const frechetDist = (curve1: Curve, curve2: Curve) => {
#   const longCurve = curve1.length >= curve2.length ? curve1 : curve2;
#   const shortCurve = curve1.length >= curve2.length ? curve2 : curve1;
#   const calcVal = (
#     i: number,
#     j: number,
#     prevResultsCol: number[],
#     curResultsCol: number[]
#   ): number => {
#     if (i === 0 && j === 0) {
#       return pointDistance(longCurve[0], shortCurve[0]);
#     }
#     if (i > 0 && j === 0) {
#       return Math.max(
#         prevResultsCol[0],
#         pointDistance(longCurve[i], shortCurve[0])
#       );
#     }
#     const lastResult = curResultsCol[curResultsCol.length - 1];
#     if (i === 0 && j > 0) {
#       return Math.max(lastResult, pointDistance(longCurve[0], shortCurve[j]));
#     }

#     return Math.max(
#       Math.min(prevResultsCol[j], prevResultsCol[j - 1], lastResult),
#       pointDistance(longCurve[i], shortCurve[j])
#     );
#   };

#   let prevResultsCol: number[] = [];
#   for (let i = 0; i < longCurve.length; i++) {
#     const curResultsCol: number[] = [];
#     for (let j = 0; j < shortCurve.length; j++) {
#       // we only need the results from i - 1 and j - 1 to continue the calculation
#       // so we only need to hold onto the last column of calculated results
#       // prevResultsCol is results[i-1][:] in the original algorithm
#       // curResultsCol is results[i][:j-1] in the original algorithm
#       curResultsCol.push(calcVal(i, j, prevResultsCol, curResultsCol));
#     }
#     prevResultsCol = curResultsCol;
#   }

#   return prevResultsCol[shortCurve.length - 1];
# };

# export default frechetDist;


def frechet_distance(curve1: Curve, curve2: Curve) -> float:
    """
    Discrete Frechet distance between 2 curves
    based on http://www.kr.tuwien.ac.at/staff/eiter/et-archive/cdtr9464.pdf
    modified to be iterative and have better memory usage
    """
    long_curve = curve1 if len(curve1) >= len(curve2) else curve2
    short_curve = curve2 if len(curve1) >= len(curve2) else curve1

    def calc_val(
        i: int, j: int, prev_results_col: list[float], cur_results_col: list[float]
    ) -> float:
        if i == 0 and j == 0:
            return point_distance(long_curve[0], short_curve[0])
        if i > 0 and j == 0:
            return max(
                prev_results_col[0], point_distance(long_curve[i], short_curve[0])
            )
        last_result = cur_results_col[-1]
        if i == 0 and j > 0:
            return max(last_result, point_distance(long_curve[0], short_curve[j]))

        return max(
            min(prev_results_col[j], prev_results_col[j - 1], last_result),
            point_distance(long_curve[i], short_curve[j]),
        )

    prev_results_col = []
    for i in range(len(long_curve)):
        cur_results_col = []
        for j in range(len(short_curve)):
            # we only need the results from i - 1 and j - 1 to continue the calculation
            # so we only need to hold onto the last column of calculated results
            # prev_results_col is results[i-1][:] in the original algorithm
            cur_results_col.append(calc_val(i, j, prev_results_col, cur_results_col))
        prev_results_col = cur_results_col

    return prev_results_col[len(short_curve) - 1]
