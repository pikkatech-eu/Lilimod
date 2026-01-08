import math
import numpy as np
import numpy.fft

"""
Iseger's coefficients for the three supported numbers of integration nodes: 16, 32, 48.
In the pair (alpha, lambda) alpha is the abscissa of the node, lambda its weight in the summation.
Borrowed from: https://www.cs.hs-rm.de/~weber/lapinv/deniseger/deniseger.htm
"""
ISEGER_COEFFICIENTS_16 = [
    (1.00000000000000, 0),
    (1.00000000000004, 6.28318530717958),
    (1.00000015116847, 12.5663706962589),
    (1.00081841700481, 18.8502914166954),
    (1.09580332705189, 25.2872172156717),
    (2.00687652338724, 34.2969716635260),
    (5.94277512934943, 56.1725527716607),
    (54.9537264520382, 170.533131190126),
]

ISEGER_COEFFICIENTS_32 = [
    (1.00000000000000, 0),
    (1.00000000000000, 6.28318530717958),
    (1.00000000000000, 12.5663706143592),
    (1.00000000000000, 18.8495559215388),
    (1.00000000000000, 25.1327412287184),
    (1.00000000000895, 31.4159265359035),
    (1.00000004815464, 37.6991118820067),
    (1.00003440685547, 43.9823334683971),
    (1.00420404867308, 50.2716029125234),
    (1.09319461846681, 56.7584358919044),
    (1.51528642466058, 64.7269529917882),
    (2.41320766467140, 76.7783110023797),
    (4.16688127092229, 96.7780294888711),
    (8.37770013129610, 133.997553190014),
    (23.6054680083019, 222.527562038705),
    (213.824023377988, 669.650134867713),
]

ISEGER_COEFFICIENTS_48 = [
    (1.00000000000000, 0),
    (1.00000000000000, 6.28318530717957),
    (1.00000000000000, 12.5663706143592),
    (1.00000000000000, 18.8495559215388),
    (1.00000000000000, 25.1327412287183),
    (1.00000000000000, 31.4159265358979),
    (1.00000000000000, 37.6991118430775),
    (1.00000000000000, 43.9822971502571),
    (1.00000000000000, 50.2654824574367),
    (1.00000000000234, 56.5486677646182),
    (1.00000000319553, 62.8318530747628),
    (1.00000128757818, 69.1150398188909),
    (1.00016604436873, 75.3984537709689),
    (1.00682731991922, 81.6938697567735),
    (1.08409730759702, 88.1889420301504),
    (1.36319173228680, 95.7546784637379),
    (1.85773538601497, 105.767553649199),
    (2.59022367414073, 119.58751936774),
    (3.73141804564276, 139.158762677521),
    (5.69232680539143, 168.156165377339),
    (9.54600616545647, 214.521886792255),
    (18.8912132110256, 298.972429369901),
    (52.7884611477405, 497.542914576338),
    (476.4483318696360, 1494.71066227687),
]

def invert \
                (
                laplace_image: callable,
                delta_t: float,
                number_of_values: int,
                critical_abscissa: float = 0,
                quadrature_degree: int = 16
        ):
    """
    Computes the values of the Laplace original for a given Laplace image
    and a sequence of values of the time argument with given step.
    :param laplace_image:       The Laplace image, F(z: complex) -> complex.
    :param delta_t:             The time step for the values of original.
    :param number_of_values:    The number of output values of the original,
                                should be a power of 2.
    :param critical_abscissa:   The critical abscissa for the Laplace image
                                which is the value of an abscissa in the complex plane
                                such that c is greater than the real part of all singularities
                                of the  Laplace image (https://en.wikipedia.org/wiki/Inverse_Laplace_transform).
    :param quadrature_degree:   The degree of Gauss quadrature (supported values are 16, 32, 48).
    :return:                    Array of values of the original function in points k * deltaT, k = 0, ..., m.
    TODO: Results are wrong; debugging needed!
    """
    if delta_t <= 0:
        raise ArithmeticError(f"The value of time step is invalid: {delta_t}.")

    if number_of_values < 2:
        raise ArithmeticError(f"The number of output values is invalid: {number_of_values} (must be >= 2).")

    if quadrature_degree not in [16, 32, 48]:
        raise ValueError(f"The number of quadrature nodes {quadrature_degree} is not supported. Must be 16, 32, or 48.")

    m = number_of_values
    mm = 2

    while mm <= number_of_values:
        mm *= 2

    if mm < number_of_values:
        mm *= 2

    number_of_values = mm
    m2 = 8 * number_of_values
    b = 44.0 / m2
    coefficients = ISEGER_COEFFICIENTS_16

    match quadrature_degree:
        case 32:
            coefficients = ISEGER_COEFFICIENTS_32
        case 48:
            coefficients = ISEGER_COEFFICIENTS_48

    y = [0.0] * (m + 1)

    image_values = [0 + 0j] * (m2 + 1)

    for k in range(m2 + 1):
        sum = 0

        for j in range(int(quadrature_degree / 2)):
            z = b + (0 + 1j) * (coefficients[j][1] + 2.0 * math.pi * k / m2)
            z = critical_abscissa + z / delta_t
            sum += coefficients[j][0] * laplace_image(z).real

        image_values[k] = 2.0 * sum / delta_t

    image_values[0] = (image_values[0] + image_values[m2]) / 2.0

    inverse_fft = numpy.fft.ifft(image_values[:m2]) * (m2 / 2)

    m4 = int(m2 / 4)

    result = [0.0] * number_of_values

    for j in range(number_of_values):
        exp_arg = b * j

        if critical_abscissa > 0:
            exp_arg += critical_abscissa * (j * delta_t)

        result[j] = inverse_fft[j].real * math.exp(exp_arg) / m4

    return result


if __name__ == '__main__':
    def image(p: complex) -> complex:
        return 1.0 / (1 + p)

    delta_t = 0.1
    number_of_values = 20
    result = invert(image, delta_t, number_of_values)

    print(result)

    for i in range(number_of_values + 1):
        iseg = result[i]
        exact = math.exp(- i * delta_t)
        diff = abs(iseg - exact)
        percent = diff * 100

        print(f"t={i * delta_t:0.1}\tiseg={iseg}\texact={exact}\tdiff={diff}\tpercent={percent}")
