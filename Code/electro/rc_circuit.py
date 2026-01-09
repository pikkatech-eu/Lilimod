import math
import numpy as np


DEFAULT_RESISTANCE  = 10000     # Ohm
DEFAULT_CAPACITY    = 1e-4      # Far

class RCCircuit:
    """
    Describes a simple RC electrical circuit under an arbitrary external voltage applied.
    """
    def __init__(self, capacity: float = DEFAULT_CAPACITY, resistance: float = DEFAULT_RESISTANCE):
        """
        Creates an instance of a simple RC electrical circuit with given parameters and computes the time constant T.
        :param capacity:
        :param resistance:
        """
        self._capacity = capacity
        self._resistance = resistance
        self.T = self._capacity * self._resistance

    def transfer_function(self, p: complex) -> complex:
        """
        Transfer function of the circuit.
        :param p: Laplace transform parameter.
        :return: Value of the transfer_function
        """
        return 1.0 / 1 + p * self.T

    def steady_discharge(self, initial_voltage: float, t_fin: float, dt: float) -> None:
        """
        Computes the process of steady discharge of the capacitor from its initial voltage
        and produces the graph.
        :param initial_voltage: the value of initial voltage, V.
        :param t_fin: final time, s.
        :param dt: temporal step, s.
        :return: None
        """
        values = []
        for t in np.arange(0, t_fin. dt):
            V = initial_voltage * math.exp(-t / self.T)
            values.append([t, V])



