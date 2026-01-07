import math
import scipy
import numpy as np
from numpy.polynomial import Polynomial
from constants import one_over_sqrt_pi

#region Error functions
def erfc(x: float) -> float:
    """
    Error function of real argument.
    Definition: Abramowitz and Steagun 7.1    (http://www.math.sfu.ca/%7Ecbm/aands/page_297.htm)
	Source:     Abramowitz and Steagun 7.1.28 (http://www.math.sfu.ca/%7Ecbm/aands/page_299.htm)
	Calculates the function directly using uniform approximations from Abramowitz and Steagun for 0 <= x <= 3.5
	and asymptotic expansions for x >= 3.5. For x < 0 erfx(x) = 2 - erfc(-x).
    :param x:   Argument
    :return:    The value of erfc.
    """
    if x < 0.0:
        return 2.0 - erfc(-x)
    elif x <= 3.5:
        return _erfc_of_small_positive(x)
    else:
        return _erfc_asymptotic(x)

def erf(x: float) -> float:
    """
    Definition: Abramowitz and Steagun 7.1.1    (http://www.math.sfu.ca/%7Ecbm/aands/page_297.htm)
    :param x:   Argument
    :return:    The value of erf.
    """
    return 1.0 - erfc(x)

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
    :return:        The value of serfc
    """
    return cerfc(z, alpha) - math.exp(-0.25 * alpha**2 / (z**2)) * erfc(z)
#endregion

#region Hantushian
def hantush(z: float, u: float) -> float:
    if z < np.finfo(np.float32):
        return (1.0 / (2 * math.pi)) * scipy.special.k0(math.sqrt(u))
    elif abs(z) < abs(u / (4.0 * z)):
        return (1.0 / (2 * math.pi)) * scipy.special.k0(math.sqrt(u)) - _hantush_series(z, u / (4.0 * z))
    else:
        return _hantush_series(u / (4.0 * z), z)

#endregion

#region Protected Auxiliary
def _erfc_of_small_positive(x: float) -> float:
    """
    Calculates the value of erfc(x) for 0.0 <= x <= 3.5
    Definition: Abramowitz and Steagun 7.1    (http://www.math.sfu.ca/%7Ecbm/aands/page_297.htm)
    Source:     Abramowitz and Steagun 7.1.28 (http://www.math.sfu.ca/%7Ecbm/aands/page_299.htm)
    :param x:   Argument
    :return:    value of erfc(x) calculated
    """
    a = [1.0, 0.0705230784, 0.0422820123, 0.0092705272, 0.00015220143, 0.0002765672, 0.0000430638]
    p = Polynomial(a)(x)
    return 1.0 / p**16

def _erfc_asymptotic(x: float) -> float:
    """
    Calculates erfc(x) for big x along with the asymptotic formula (7.1.23) from Abramowitz & Steagun
	with a given number of terms in the asymptotic expansion.
    :param x:   Argument
    :return:    Asymptotic approximation for erfc(x)
    """
    sum = 1.0
    u = 0.5 / x**2
    term = -u

    number_of_terms = 5

    for m in range(1, number_of_terms):
        sum += term
        term *= -term * (2 * m + 1) * u

        return sum * one_over_sqrt_pi * math.exp(-x**2) / x

def _hantush_series(p: float, q: float) -> float:
    """
    Calculates the sum of the series \$  \frac{1}{4 \pi} \sum \limits_{n=0}^\infty \frac{(-1)^n}{n!} p^n E_{n+1}(q) \$
    :param p:   Argument acting as the argument of the power series
    :param q:   Argument of the integral exponential \$  E_{n+1} \$
    :return:    Value of the Hantush series, if q > 0, Float.PositiveInfinity otherwise.
    """
    if q <= 0:
        return float('inf')

    result = 0.0
    factor = 1.0
    n = 0

    E = scipy.special.exp1(q)
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
    z = 0.5 + 0.6j

    r = scipy.special.iv(4, z)

    print(r)