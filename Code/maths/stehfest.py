import math

FAIRS_OPTIMUM_ORDER = 14

class Stehfest:
    """
    Stehfest's numerical Laplace inverter.
	"Harald Stehfest. Numerical Inversion of Laplace Transforms [D5]. Communications of the ACM Volume 13/Number 1/January, 1970".
	Code for the Initialize() and InverseTransform() routines borrowed creatively from Walt Fair's example
	(http://www.codeproject.com/Articles/25189/Numerical-Laplace-Transforms-and-Inverse-Transform).
    """
    def __init__(self, order: int = FAIRS_OPTIMUM_ORDER):
        """
        Order constructor.
		Initializes the coefficient arrays with given order.
        :param order:   Inversion order (recommended: as a rule, not more than 12..16).
        """
        self._order = order
        self._initialize()

    def invert(self, image: callable, t: float) -> float:
        """
        Calculates the value of the original by inverting the Laplace image.
        :param image:   Function calculating the Laplace image.
        :param t:       Value of time.
        :return:        Approximation  to the value of the original with the given value of time.
        """
        ln2t = math.log(2) / t
        x = 0
        y = 0

        for i in range(len(self._coefficients)):
            x += ln2t
            y += self._coefficients[i] * image(x)

        return ln2t * y

    #region Protected Auxiliary
    def _initialize(self):
        """
        Initialization of the Stehfest's coefficients.
        Borrowed from Walt Fair.
        :return: None.
        """
        N2 = int(self._order / 2)
        NV = int(2 * N2)

        self._coefficients  = [0.0] * NV

        sign = 1
        if (N2 % 2) != 0:
            sign = -1

        for i in range(NV):
            kmin = int((i + 2) / 2)
            kmax = i + 1
            if kmax > N2:
                kmax = N2

            sign = -sign

            for k in range(kmin, kmax + 1):
                self._coefficients[i] = (self._coefficients[i] + (math.pow(k, N2) / math.factorial(k)) *
                                         (math.factorial(2 * k) / math.factorial(2 * k - i - 1)) /
                                         math.factorial(N2 - k) / math.factorial(k - 1) / math.factorial(i + 1 - k))

            self._coefficients[i] = sign * self._coefficients[i]

    #endregion

if __name__ == '__main__':
    def image(p: float) -> float:
        return 1.0 / (1 + p)

    sf = Stehfest(6)

    t = 1

    value = sf.invert(image, t)

    print(value, math.exp(-t))

    t = 0.001
    while t < 5:
        value = sf.invert(image, t)
        expected = math.exp(-t)
        delta = value - expected
        percent = delta * 100

        print(t, percent)
        t += 0.2