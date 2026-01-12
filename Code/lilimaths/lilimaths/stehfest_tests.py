import math

import numpy as np

from curve import Curve
from stehfest import Stehfest
from liliutils.plotter2 import Plotter


def test_context(image: callable, orders: list[int], expected: callable, t_fin: float, dt: float, **kwargs):
    """
    Tests Stehfest's method for an image-original pair.
    Creates a series of approximate originals with different values of N against the exact original and puts them to a graph.
    Creates a series of percentual approximation error with different values of N and puts them to a graph.
    @param image:       Laplace image F(p), p: float
    @param orders:      List of values of integration order (each of which must be even)
    @param expected:    Expected (exact) original: Float-> float
    @param t_fin:       Final time
    @param dt:          Time step.
    @return:            None.
    """
    curves = list[Curve]()
    values = []

    for t in np.arange(dt, t_fin + dt, dt):
        values.append((t, expected(t)))

    exact_curve = Curve()
    exact_curve.values  = values
    exact_curve.label   = "Exact"
    exact_curve.color   = 'red'

    curves.append(exact_curve)

    for N in orders:
        sf = Stehfest(N)
        values = []
        for t in np.arange(dt, t_fin + dt, dt):
            values.append((t, sf.invert(image, t)))

        curve = Curve()
        curve.values = values
        curve.label = f"N = {N}"
        curve.color = 'blue'

        curves.append(curve)

    # Visualisation
    plotter = Plotter(**kwargs)

    plotter.plot(curves)


if __name__ == '__main__':
    def exponent_image(p: float) -> float:
        return 1 / (1 + p)

    def exponent_expected(t: float) -> float:
        return math.exp(-t)

    t_fin = 5
    dt = 0.01
    test_context(exponent_image, [6, 8, 10], exponent_expected, t_fin, dt, min_x=dt, max_x=t_fin, digits_x=0, major_step_x = 1, minor_step_x = 0.2)

