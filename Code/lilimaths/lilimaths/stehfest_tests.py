from math import exp, sin, pi, sqrt

import numpy as np
import scipy.special

from curve import Curve
from stehfest import Stehfest
from liliutils.plotter2 import Plotter

COLORS = ['red', 'blue', 'green', 'black', 'magenta', 'gray', 'orange']

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
    exact_curve.color   = COLORS[0]

    curves.append(exact_curve)

    color_index = 1
    for N in orders:
        sf = Stehfest(N)
        values = []
        for t in np.arange(dt, t_fin + 5 * dt, 5 * dt):
            values.append((t, sf.invert(image, t)))

        curve = Curve()
        curve.values = values
        curve.label = f"N = {N}"
        curve.color = COLORS[color_index]
        curve.kind = 'scatter'
        color_index += 1

        curves.append(curve)

    # Visualisation
    plotter = Plotter(**kwargs)

    plotter.plot(curves)


if __name__ == '__main__':
    def exponent_image(p: float) -> float:
        return 1 / (1 + p)

    def exponent_original(t: float) -> float:
        return exp(-t)

    def decaying_sine_image(p: float) -> float:
        return 1 / (1 + (p + 0.5)**2)

    def decaying_sine_original(t: float) -> float:
        return exp(-0.5 * t) * sin(t)

    def linear_image(p: float) -> float:
        return 1 / p**2

    def linear_original(t: float) -> float:
        return t

    def exponent_multiplied_image(p: float) -> float:
        return 1 / (p + 1)**2

    def exponent_multiplied_original(t: float) -> float:
        return t * exp(-t)

    def rectangular_wave_image(p: float) -> float:
        return exp(-p) / p

    def rectangular_wave_origin(t: float) -> float:
        return 0 if t <= 1 else 1

    def rectangular_wave2_origin(t: float) -> float:
        return 1 if 1 <= t <= 2 else 0

    def rectangular_wave2_image(p: float) -> float:
        return (exp(-p) - exp(-(p * 2)))/ p

    k = 1
    def k0_image(p: float) -> float:
        return (1 / p) * scipy.special.k0(sqrt(k * p))

    def k0_original(t: float) -> float:
        return 0.5 * scipy.special.exp1(k / t)

    images              = [
                            exponent_image,
                            decaying_sine_image,
                            linear_image,
                            exponent_multiplied_image,
                            rectangular_wave_image,
                            rectangular_wave2_image,
                            k0_image
                          ]

    originals           = [
                            exponent_original,
                            decaying_sine_original,
                            linear_original,
                            exponent_multiplied_original,
                            rectangular_wave_origin,
                            rectangular_wave2_origin,
                            k0_original
                          ]

    titles              = [
                            "Exponential decay",
                            "Sinusoidal decay",
                            "Linear function",
                            "Exponent multiplied",
                            "Rectangular wave",
                            "Finite rectangular wave",
                            "Well function"
                          ]

    original_equations  = [
                            'exp(-t)',
                            'exp(-0.5t) * sin (t)',
                            't',
                            't * exp(-t)',
                            'H(t-1)',
                            'H(t-1) - H(t-2)',
                            'E1(k/t) / (4 pi)'
                          ]

    t_fin = 5
    dt = 0.01
    context_index = 6

    test_context(images[context_index], [2, 4, 6, 12], originals[context_index], t_fin, dt,
                 size = (8, 6),
                 min_x=dt,
                 max_x=t_fin,
                 min_y = -0.2,
                 max_y = 1.2,
                 digits_x=0,
                 major_step_x = 1,
                 minor_step_x = 0.2,
                 major_step_y=0.2,
                 minor_step_y=0.1,
                 title=titles[context_index],
                 label_x = 't',
                 label_y = f'f(t) = {original_equations[context_index]}'
                 )

