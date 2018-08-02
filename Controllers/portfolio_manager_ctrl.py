import random

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class PortfolioManagerCtrl:
    def __init__(self):
        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)

    def get_canvas(self):
        return self.canvas

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data

        ax.plot(data, '*-')
    # plt.plot([1,2],[1,2])

        # refresh canvas
        self.canvas.draw()