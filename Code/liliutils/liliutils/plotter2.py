import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from lilimaths.curve import Curve

#region default values
DEFAULT_SIZE = (8, 8)

DEFAULT_MIN_X           = 0
DEFAULT_MAX_X           = 1

DEFAULT_MAJOR_STEP_X    = 0.1
DEFAULT_MINOR_STEP_X    = 0.05

DEFAULT_DIGITS_X        = 1

DEFAULT_MIN_Y           = 0
DEFAULT_MAX_Y           = 1

DEFAULT_MAJOR_STEP_Y    = 0.1
DEFAULT_MINOR_STEP_Y    = 0.05

DEFAULT_DIGITS_Y        = 1

DEFAULT_LABEL_X         = "X"
DEFAULT_LABEL_Y         = "Y"

DEFAULT_TITLE           = ""
DEFAULT_LABEL           = ""

DEFAULT_CURVE_COLOR     = 'blue'
DEFAULT_CURVE_WIDTH     = 1.5
#endregion

class Plotter:
    """
    Provides a tool to plot curve graphs.
    """
    def __init__(self, **kwargs):
        """
        :param kwargs: Dictionary of plotting parameters.
            Parameters:
            ==========
            'size'          Size of plot area, inch * inch. Default: (8, 8)
            'min_x'         Minimum value of X (X-axis). Default: 0
            'max_x'         Maximum value of X (X-axis). Default: 1
            'major_step_x'  Major grid step on X axis. Default: 0.1
            'minor_step_x'  Minor grid step on X axis. Default: 0.05
            'digits_x'      Number of digits for the characters on X axis. Default: 1
            'min_y'         Minimum value of Y (Y-axis). Default: 0
            'max_y'         Maximum value of Y (Y-axis). Default: 1
            'major_step_y'  Major grid step on Y axis. Default: 0.1
            'minor_step_y'  Minor grid step on Y axis. Default: 0.05
            'digits_y'      Number of digits for the characters on Y axis. Default: 1
            'label_x'       Label of the X axis. Default: 'X'.
            'label_y'       Label of the Y axis. Default: 'Y'.
            'title'         The title of the diagram. Default: empty string.
        :return: None
        """
        self._parameters = kwargs
        self._set_defaults()
        self._prepare_canvas()

    def plot(self, curves = list[Curve]):
        """
        Plots curve graphs for a list of curves.
        :param curves: The list of curves.
        :return: None
        """
        for curve in curves:
            x = [t[0] for t in curve.values]
            y = [t[1] for t in curve.values]

            if curve.kind == 'line':
                self._ax.plot(x, y, linewidth=self._parameters['curve_width'], label=curve.label, antialiased=True, color=curve.color)
            else:
                self._ax.scatter(x, y, color=curve.color, marker=curve.marker, linewidth=0.5, label=curve.label, antialiased=True)

        self._ax.legend(loc='best')

        plt.show()

    #region Protected auxiliary
    def _set_defaults(self):
        self._parameters.setdefault('size', DEFAULT_SIZE)
        self._parameters.setdefault('min_x', DEFAULT_MIN_X)
        self._parameters.setdefault('max_x', DEFAULT_MAX_X)
        self._parameters.setdefault('major_step_x', DEFAULT_MAJOR_STEP_X)
        self._parameters.setdefault('minor_step_x', DEFAULT_MINOR_STEP_X)
        self._parameters.setdefault('digits_x', DEFAULT_DIGITS_X)
        self._parameters.setdefault('min_y', DEFAULT_MIN_Y)
        self._parameters.setdefault('max_y', DEFAULT_MAX_Y)
        self._parameters.setdefault('major_step_y', DEFAULT_MAJOR_STEP_Y)
        self._parameters.setdefault('minor_step_y', DEFAULT_MINOR_STEP_Y)
        self._parameters.setdefault('digits_y', DEFAULT_DIGITS_Y)
        self._parameters.setdefault('label_x', DEFAULT_LABEL_X)
        self._parameters.setdefault('label_y', DEFAULT_LABEL_Y)
        self._parameters.setdefault('title', DEFAULT_TITLE)
        self._parameters.setdefault('label', DEFAULT_LABEL)
        self._parameters.setdefault('curve_color', DEFAULT_CURVE_COLOR)
        self._parameters.setdefault('curve_width', DEFAULT_CURVE_WIDTH)

    def _prepare_canvas(self):
        plt.rc('figure', figsize=self._parameters['size'])

        fig, ax = plt.subplots(1, 1)

        self._ax = ax

        ax.set_xlim(self._parameters['min_x'], self._parameters['max_x'])
        ax.xaxis.set_major_locator(MultipleLocator(self._parameters['major_step_x']))
        ax.xaxis.set_major_formatter(f'{{x:.{self._parameters['digits_x']}f}}')
        ax.xaxis.set_minor_locator(MultipleLocator(self._parameters['minor_step_x']))

        ax.set_ylim(self._parameters['min_y'], self._parameters['max_y'])
        ax.yaxis.set_major_locator(MultipleLocator(self._parameters['major_step_y']))
        ax.yaxis.set_major_formatter(f'{{x:.{self._parameters['digits_y']}f}}')
        ax.yaxis.set_minor_locator(MultipleLocator(self._parameters['minor_step_y']))

        ax.set_xlabel(self._parameters['label_x'])
        ax.set_ylabel(self._parameters['label_y'])

        ax.set_title(self._parameters['title'])

        plt.grid(visible=True, which='major', color='b', alpha=0.25, linestyle='-', linewidth=0.75)
        plt.grid(visible=True, which='minor', color='r', alpha=0.15, linestyle='-', linewidth=0.5)

        # Emphasize the x = 0 axis.
        ax.axhline(y=0, color='k', linewidth=0.5)
    #endregion

if __name__ == '__main__':

    curves = []

    values = []
    for t in np.arange(0, 2.0, 0.01):
        values.append((t, t**2))

    curve = Curve()
    curve.values = values
    curve.label = 'x^2'
    curve.color = 'green'

    curves.append(curve)

    values = []
    for t in np.arange(0, 2.0, 0.01):
        values.append((t, (0.85 * t ** 3) * abs(math.sin(3 * t))))

    curve = Curve()
    curve.values = values
    curve.label = '0.5 * x^3'
    curve.color = 'red'

    curves.append(curve)

    plotter = Plotter(max_x=2, max_y=10, major_step_y=1, minor_step_y = 0.1, digits_y=0)

    plotter.plot(curves)