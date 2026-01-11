import numpy as np

from curve import Curve
from stehfest import Stehfest


def test_context(image: callable, orders: list[int], expected: callable, t_fin: float, dt: float ):
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

    for t in np.arange(0, t_fin + dt, dt):
        values.append(t, expected(t))

    exact_curve = Curve()
    exact_curve.values  = values
    exact_curve.label   = "Exact"
    exact_curve.color   = 'red'

    curves.append(exact_curve)

    for N in orders:
        sf = Stehfest(N)
        values = []
        for t in np.arange(0, t_fin + dt, dt):
            values.append(t, sf.invert(image, t))

        curve = Curve()
        curve.values = values
        curve.label = f"N = {N}"
        curve.color = 'blue'

        curves.append(curve)


    # visualization

