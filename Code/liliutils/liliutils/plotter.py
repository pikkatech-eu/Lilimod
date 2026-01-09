import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

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

class Plotter:
    def plot(self, data: list[(float, float)], **kwargs) -> None:
        """
        Plots a simple graph using simple data list.
        :param data: list of data pairs: (t, f(t)).
        :param kwargs: Dictionary of plotting parameters.
            Parameters:
            ==========
            "size"      Size of plot area, inch * inch. Default: (8, 8)
        :return: None
        """
        #region Setting parameters
        size            = kwargs.get("size", DEFAULT_SIZE)

        x_min           = kwargs.get("x_min", DEFAULT_MIN_X)
        x_max           = kwargs.get("x_max", DEFAULT_MAX_X)
        step_x_major    = kwargs.get("step_x_major", DEFAULT_MAJOR_STEP_X)
        step_x_minor    = kwargs.get("step_x_minor", DEFAULT_MINOR_STEP_X)

        digits_x        = kwargs.get("digits_x", DEFAULT_DIGITS_X)
        digits_y        = kwargs.get("digits_y", DEFAULT_DIGITS_Y)

        y_min           = kwargs.get("y_min", DEFAULT_MIN_Y)
        y_max           = kwargs.get("y_max", DEFAULT_MAX_Y)
        step_y_major    = kwargs.get("step_y_major", DEFAULT_MAJOR_STEP_Y)
        step_y_minor    = kwargs.get("step_y_minor", DEFAULT_MINOR_STEP_Y)

        label_x         = kwargs.get("label_x", DEFAULT_LABEL_X)
        label_y         = kwargs.get("label_y", DEFAULT_LABEL_Y)

        title           = kwargs.get("title", DEFAULT_TITLE)
        label           = kwargs.get("label", DEFAULT_LABEL)

        curve_color     = kwargs.get("curve_color", DEFAULT_CURVE_COLOR)
        curve_width     = kwargs.get("curve_width", DEFAULT_CURVE_WIDTH)
        #endregion

        # Set default figure size (8x8 inches).
        plt.rc('figure', figsize=size)

        # Create a figure with one plot.
        fig, ax = plt.subplots(1, 1)

        ## Set the properties of the x axis:
        # The major step is 1.0 s; the minor one 0.2 s.
        ax.set_xlim(x_min, x_max)
        ax.xaxis.set_major_locator(MultipleLocator(step_x_major))
        ax.xaxis.set_major_formatter(f'{{x:.{digits_x}f}}')
        ax.xaxis.set_minor_locator(MultipleLocator(step_x_minor))

        ## Set the properties of the y axis:
        # The major step is 2.0 V; the minor one 0.5 V.
        ax.set_ylim(y_min, y_max)
        ax.yaxis.set_major_locator(MultipleLocator(step_y_major))
        ax.yaxis.set_major_formatter(f'{{x:.{digits_y}f}}')
        ax.yaxis.set_minor_locator(MultipleLocator(step_y_minor))

        # Set the axis labels
        ax.set_xlabel(label_x)
        ax.set_ylabel(label_y)

        # Set the title
        ax.set_title(title)

        # Set the properties of the grid: the major lines are blue, the minor ones red.
        plt.grid(visible=True, which='major', color='b', alpha=0.25, linestyle='-', linewidth=0.75)
        plt.grid(visible=True, which='minor', color='r', alpha=0.15, linestyle='-', linewidth=0.5)

        # Emphasize the x = 0 axis.
        ax.axhline(y=0, color='k', linewidth=0.5)

        x = [t[0] for t in data]
        y = [t[1] for t in data]

        # Plot the theoretical curve.
        ax.plot(x, y, linewidth=curve_width, label=label, antialiased=True, color=curve_color)

        # Place the legend.
        ax.legend(loc='best')

        plt.show()

if __name__ == '__main__':
    data = []

    for t in np.arange(0, 1.01, 0.01):
        V = 1.00 * math.exp(-2 * t)
        data.append((t, V))

    plotter = Plotter()

    plotter.plot(data, title="test!", x_min=0, x_max=1, y_min=0, y_max=1, curve_width=3, curve_color='red')