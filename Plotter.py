import warnings

from Visualizer import Visualizer as VS
from pyqtgraph.Qt import QtGui, QtCore
from main import prgname, vrs
from loguru import logger
import pyqtgraph as pg
import numpy as np
import time

prev_s1 = prev_vis = np.array


class Plotter:
    running = False
    dimx, dimy = [0,1024], [-0.1, 0.1]
    cut = 3
    vis_cut = 5

    def __init__(self, dimy=[-0.01, 0.01], dimx=[0,1024]):
        self.dimx[0] = dimx[0]
        self.dimx[1] = int(dimx[1]/self.cut)
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
        p3 = win.addPlot(title="Visualizer")
        win.nextRow()
        p2 = win.addPlot(title="Waveform")
        # set p1 & p2 limits
        p1.setRange(xRange=self.dimx, yRange=self.dimy)
        p1.disableAutoRange()
        p3.setRange(xRange=[self.dimx[0], self.dimx[1]/self.vis_cut], yRange=[0, 0.06])
        p3.disableAutoRange()
        p2.setRange(xRange=[0, self.v.chunksize], yRange=[-0.5, 0.5])
        p2.disableAutoRange()

        i = 0
        logger.debug("Plotting is live")
        warnings.filterwarnings('ignore')

        def update():
            global prev_s1, prev_vis
            try:
                chunk = np.array(self.v.get_chunk()[0]).astype(float)
            except Exception as err:
                logger.warning("Failed to convert complex chunk, retrying..")
                return
            try:
                spectrum = np.fft.ifft2(chunk).astype(float)
            except RuntimeWarning:
                logger.warning("Complex chunk conversion failed, retrying..")
                return
            spectrum = spectrum[:int(len(spectrum)/self.cut)]
            spectrum = [np.sum(x)/2 for x in spectrum]

            p1.plot(spectrum, clear=True, pen=(255, 0, 0))

            if i % 5 == 0:
                # plot p2
                test = [np.sum(x)/2 for x in chunk]
                vis = np.absolute(spectrum)
                vis = vis[:int(len(spectrum)/self.cut*self.vis_cut)]
                for k, e in enumerate(vis):
                    if float(vis[k]) > float(prev_vis[k]):
                        prev_vis[k] = vis[k]
                local_vis = np.array(([e-e/40 for e in prev_vis]))
                p2.plot(test, clear=True, pen=(0, 255, 0))
                p3.plot(vis, clear=True, pen=(0, 0, 255), fillLevel=0, brush=(0, 0, 255, 200))
                p3.plot(local_vis, clear=False, pen=(0, 50, 100), fillLevel=0, brush=(0, 0, 255, 50))
                logger.trace("~{} chunks with avg: {}".format(self.dimx[1], sum(chunk) / len(chunk)))
                max = 0
                for v in vis:
                    if abs(v > max):
                        max = v
                mrange = float(p3.getAxis("left").range[1])
                if max > mrange:
                    p3.setRange(yRange=[0, (mrange + mrange/10)])
                else:
                    p3.setRange(yRange=[0, (mrange - mrange/12)])
                prev_s1 = spectrum
                prev_vis = local_vis

            # plot p1
            # time.sleep(0.01)





        timer = QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(0)

        global prev_s1, prev_vis
        prev_s1 = np.zeros((self.dimx[1], ))
        prev_vis = np.zeros((self.dimx[1], ))
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