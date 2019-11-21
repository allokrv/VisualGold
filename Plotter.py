from Visualizer import Visualizer as VS
from pyqtgraph.Qt import QtGui, QtCore
from main import prgname, vrs
from loguru import logger
import pyqtgraph as pg
import numpy as np
import time


class Plotter:
    running = False
    dimx, dimy = [0,1024], [-0.1, 0.1]

    def __init__(self, dimy=[-0.008, 0.008], dimx=[0,1024]):
        self.dimx[0] = dimx[0]
        self.dimx[1] = int(dimx[1]/2.5)
        self.dimy = dimy
        logger.debug("FFT in: {}x{}".format(self.dimx, self.dimy))

    def start(self):
        # logger.debug("Plotting Thread starting..")
        # create window and plot
        win = pg.GraphicsWindow(prgname)
        # pg.setConfigOptions(antialias=True)
        win.setWindowTitle("{} v{}".format(prgname, vrs))
        # create plots
        p1 = win.addPlot(title="Spectrum")
        win.nextRow()
        p2 = win.addPlot(title="Waveform")
        # set p1 & p2 limits
        p1.setRange(xRange=self.dimx, yRange=self.dimy)
        p1.disableAutoRange()
        p2.setRange(xRange=[0, self.v.chunksize], yRange=[-2, 2])
        p2.disableAutoRange()

        i = 0
        logger.debug("Plotting is live")

        def update():
            chunk = np.array(self.v.get_chunk()[0]).astype(float)
            spectrum = np.fft.ifft2(chunk).astype(float)
            spectrum = spectrum[:int(len(spectrum)/2)]
            spectrum = [np.sum(x) for x in spectrum]

            p1.plot(spectrum, clear=True, pen=(255, 0, 0))

            if i % 50 == 0:
                # plot p2
                test = [np.sum(x) for x in chunk]
                p2.plot(test, clear=True, pen=(0, 255, 0))
                logger.trace("~{} chunks with avg: {}".format(self.dimx[1], sum(chunk) / len(chunk)))

            # plot p1
            # time.sleep(0.01)

        timer = QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(1)

        QtGui.QApplication.instance().exec_()

    def start_thread(self, v):
        if type(v) != VS:
            logger.warning("Parameter v in Plotter:start_thread(v) has a wrong struct")
            return
        """ animation test
        fig, ax = plt.subplots()
        def task(i):
            ax.cla()
            chunk = v.get_chunk()[0]
            ax.plot(chunk, ",-")
            ax.set_ylim([-0.1, 0.1], auto=False)
            ax.set_xlim([self.dimx[0], self.dimx[1]], auto=False)
        ani = animation.FuncAnimation(fig, task, interval=1)
        plt.show()
        time.sleep(20)
        exit(0)
        """
        self.v = v
        self.running = True
        self.start()
        # pt = threading.Thread(target=self.start)
        # pt.start()