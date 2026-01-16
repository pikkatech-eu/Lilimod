from math import exp, sin, pi, sqrt
import cmath

import numpy as np
import scipy.special

from curve import Curve
from deviations import Deviations
from iseger import invert
from liliutils.plotter2 import Plotter

COLORS = ['red', 'blue', 'green', 'black', 'magenta', 'gray', 'orange']

def test_context(image: callable, expected: callable, dt: float, number_of_points: int, critical_abscissa:float =0, quadrature_order = 16, **kwargs):
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
    inverted = invert(image, dt, number_of_points, critical_abscissa, quadrature_order)

    max_difference = 0
    values = []
    for i in range(len(inverted)):
        inverted_value = inverted[i]
        exact_value = expected(dt * i)
        values.append((i * dt, inverted_value))

        difference = abs(inverted_value - exact_value)
        if difference > max_difference:
            max_difference = difference

    curve = Curve()
    curve.values = values
    curve.label = "den Iseger"
    curve.color = 'blue'
    curve.kind = 'scatter'

    curves.append(curve)

    values = []
    for i in range(len(curve.values) + 1):
        values.append((dt * i, expected(dt * i)))

    exact_curve = Curve()
    exact_curve.values  = values
    exact_curve.label   = "Exact"
    exact_curve.color   = COLORS[0]

    curves.append(exact_curve)

    # Visualisation
    plotter = Plotter(**kwargs)

    plotter.plot(curves)

    print(max_difference)

if __name__ == '__main__':
    def exponent_image(p: complex) -> complex:
        return 1 / (1 + p)

    def exponent_original(t: float) -> float:
        return exp(-t)

    def sine_image(p: complex) -> complex:
        return 1 / (1 + p**2)

    def sine_original(t: float) -> float:
        return sin(t)

    def damped_sine_image(p: complex) -> complex:
        return 1 / (1 + (p + 0.2)**2)

    def damped_sine_original(t: float) -> float:
        return exp(-0.2 * t) * sin(t)

    def linear_image(p: complex) -> complex:
        return 1 / p**2

    def linear_original(t: float) -> float:
        return t

    def exponent_multiplied_image(p: complex) -> complex:
        return 1 / (p + 1)**2

    def exponent_multiplied_original(t: float) -> float:
        return t * exp(-t)

    def rectangular_wave_image(p: complex) -> complex:
        return cmath.exp(-p) / p

    def rectangular_wave_origin(t: float) -> float:
        return 0 if t <= 1 else 1

    def rectangular_wave2_origin(t: complex) -> complex:
        return 1 if 1 <= t <= 2 else 0

    def rectangular_wave2_image(p: float) -> float:
        return (cmath.exp(-p) - cmath.exp(-(p * 2)))/ p

    k = 0.8
    def k0_image(p: complex) -> complex:
        return (1 / p) * scipy.special.kv(0, 2 * cmath.sqrt(k * p))

    def k0_original(t: float) -> float:
        return 0.5 * scipy.special.exp1(k / (t + 0.0001))

    a = -0.1
    def exponential_growth_image(p: complex) -> complex:
        return (1 / p) * (1 /(p + a))

    def exponential_growth_original(t: float) -> float:
        return (1 / a) * (1 - exp(- a * t))

    def exponential_growth_integrated_image(p: complex) -> complex:
        return (1 / p**2) * (1 /(p + a))

    def exponential_growth_original_integrated(t: float) -> float:
        return (t / a) - (1 / a**2) * (1 - exp(- a * t))

    images              = [
                            exponent_image,
                            sine_image,
                            damped_sine_image,
                            linear_image,
                            exponent_multiplied_image,
                            rectangular_wave_image,
                            rectangular_wave2_image,
                            k0_image,
                            exponential_growth_image,
        exponential_growth_integrated_image
                          ]

    originals           = [
                            exponent_original,
                            sine_original,
                            damped_sine_original,
                            linear_original,
                            exponent_multiplied_original,
                            rectangular_wave_origin,
                            rectangular_wave2_origin,
                            k0_original,
                            exponential_growth_original,
        exponential_growth_original_integrated
                          ]

    titles              = [
                            "Exponential decay",
                            "Sine curve",
                            "Damped sine",
                            "Linear growth",
                            "Asymmetric distribution",
                            "Delayed step function",
                            "Rectangular wave",
                            "Well function",
                            "Exponential growth",
        "Exponential growth integrated"
                          ]

    original_equations  = [
                            'exp(-t)',
                            'sin (t)',
                            'exp(-0.2t) * sin (t)',
                            't',
                            't * exp(-t)',
                            'H(t-1)',
                            'H(t-1) - H(t-2)',
                            '0.5 * E1(k/t) / (4 pi)',
                            '(1/a) * (1-exp(-at))',
        't/a - (1/a^2) (1-exp(-at))'
                          ]

    dt = 0.05
    number_of_points =100
    context_index = 9
    test_context(images[context_index], originals[context_index], dt, number_of_points, 0, quadrature_order=16,
                 size=(8, 6),
                 max_x= 5,
                 major_step_x = 1,
                 minor_step_x = 0.5,

                 major_step_y=2,
                 minor_step_y=1,
                 min_y=-0,
                 max_y=20,
                 digits_x = 0,
                 digits_y=1,
                 title=titles[context_index],
                 label_x='t',
                 label_y=f'f(t) = {original_equations[context_index]}'
                 )



