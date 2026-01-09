import math
import scipy
import numpy as np
from scipy.special import erfc, exp1, k0
from numpy.polynomial import Polynomial
from .constants import one_over_sqrt_pi

#region Error functions
def ierfc(x: float) -> float:
    """
    Repeated Integral of the Error function of real argument.
	Definition: Abramowitz & Steagun 7.2    (http://www.math.sfu.ca/%7Ecbm/aands/page_299.htm)
	Source:     Abramowitz & Steagun 7.2.1  (http://www.math.sfu.ca/%7Ecbm/aands/page_299.htm)
    :param x:   Argument
    :return:    The value of ierfc.
    """
    return one_over_sqrt_pi * math.exp(-x**2) - x * erfc(x)

def i2erfc(x: float) -> float:
    """
    Doubly Repeated Integral of the Error function of real argument.
	Definition: Abramowitz & Steagun 7.2    (http://www.math.sfu.ca/%7Ecbm/aands/page_299.htm)
	Source:     Abramowitz & Steagun 7.2.1  (http://www.math.sfu.ca/%7Ecbm/aands/page_299.htm)
    :param x:   Argument
    :return:    The value of i2erfc.
    """
    return 0.25 * (erfc(x) - 2.0 * x * ierfc(x))

def inerfc(x: float, n: int) -> float:
    """
    Repeated Integral of the Error function of real argument.
	Definition: Abramowitz & Steagun 7.2    (http://www.math.sfu.ca/%7Ecbm/aands/page_299.htm)
	Source:     Abramowitz & Steagun 7.2.1  (http://www.math.sfu.ca/%7Ecbm/aands/page_299.htm)
    :param x:   Argument
    :param n:   Function Order
    :return:    The value of inerfc.
    """
    match n:
        case -1:
            return one_over_sqrt_pi * math.exp(-x**2)
        case 0:
            return erfc(x)
        case 1:
            return ierfc(x)
        case 2:
            return i2erfc(x)
        case _:
            return (0.5 * inerfc(x, n - 2) - x * inerfc(x, n - 1)) / n
#endregion

#region Diffusion functions
def cerfc(z: float, alpha: float) -> float:
    """
    Diffusion cosine, or Hantush's first depletion function.
	Source: Hantush, M.S., "Nonsteady Flow to Flowing Wells in Leaky Aquifers." Jour. Geophys. Res., 64, 8, 1043-1052. 1959.
    :param z:       Argument
    :param alpha:   Parameter
    :return:        The value of cerfc
    """
    if abs(z) < np.finfo(float).eps:
        return math.exp(-alpha)

    argument = z - 0.5 * alpha / z
    result = math.exp(-alpha) * erfc(argument)

    argument = z + 0.5 * alpha / z
    result += math.exp(alpha) * erfc(argument)
    result /= 2.0
    return result

def serfc(z: float, alpha: float) -> float:
    """
    Diffusion sine, or Hantush's second depletion function.
	Source: Hantush, M. S., "Nonsteady Flow to Flowing Wells in Leaky Aquifers." Jour. Geophys. Res., 64, 8, 1043-1052. 1959.
    :param z:       Argument
    :param alpha:   Parameter
    :return:        The value of serfc
    """
    if abs(z) < np.finfo(float).eps:
        return math.exp(-alpha)

    argument = z + 0.5 * alpha / z
    result = math.exp(-alpha) * erfc(argument)

    argument = z + 0.5 * alpha / z
    result += math.exp(alpha) * erfc(argument)
    result /= 2.0
    return result

def aerfc(z: float, alpha: float) -> float:
    """
    "aerreal" error function. Called so because it occurs in calculations for linear and areal water intakes
    in leaky and non-leaky homogeneous aquifers.
	Inverse Laplace transform of exp(-z * sqrt(p/a + g^2)) / (p (p/a + g^2)) is
	(1/g^2) * aerfc(z/2 sqrt(at), g * z).
    :param z:       Argument
    :param alpha:   Parameter
    :return:        The value of aerfc.
    """
    return cerfc(z, alpha) - math.exp(-0.25 * alpha**2 / (z**2)) * erfc(z)
#endregion

#region Hantushian
def hantush(z: float, u: float) -> float:
    if z < np.finfo(np.float32):
        return (1.0 / (2 * math.pi)) * k0(math.sqrt(u))
    elif abs(z) < abs(u / (4.0 * z)):
        return (1.0 / (2 * math.pi)) * k0(math.sqrt(u)) - _hantush_series(z, u / (4.0 * z))
    else:
        return _hantush_series(u / (4.0 * z), z)

#endregion

#region Protected Auxiliary
def _hantush_series(p: float, q: float) -> float:
    """
    Calculates the sum of the series $  \frac{1}{4 \pi} \sum \limits_{n=0}^\infty \frac{(-1)^n}{n!} p^n E_{n+1}(q) $
    :param p:   Argument acting as the argument of the power series
    :param q:   Argument of the integral exponential $  E_{n+1} $
    :return:    Value of the Hantush series, if q > 0, Float.PositiveInfinity otherwise.
    """
    if q <= 0:
        return float('inf')

    result = 0.0
    factor = 1.0
    n = 0

    E = exp1(q)
    term = float('inf')
    epsilon = min(np.finfo(np.float32), math.exp(-p) * E)

    while abs(term) > epsilon:
        term = factor * E
        result += term

        n += 1
        factor = -factor * p / n
        E = (math.exp(-q) - q * E) / n

    result /= (4 * math.pi)

    return result
#endregion

if __name__ == '__main__':

    t = 0.5
    print(ierfc(t), erfc(t))