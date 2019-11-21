from loguru import logger
import Visualizer
import argparse
import Plotter
import time
import sys

prgname = "VisualGold"
vrs = "0.21"

apars = argparse.ArgumentParser(description="{} for Windows (Python3)".format(prgname))
apars.add_argument('-V', '--version',
                   action='version', version="{0} {1}".format(prgname, vrs),
                   help="Displays current version")
apars.add_argument('-v', '--verbose',
                   action='store_true',
                   help="Sets logger level to show debug info")
apars.add_argument('-x', '--xtreme',
                   action='store_true',
                   help="Sets logger level to show even more debug")
args = apars.parse_args()


if __name__ == '__main__':
    logger.remove(0)
    verbose = args.verbose
    if verbose:
        logger.debug("Verbose mode: on")
        if args.xtreme:
            logger.add(sys.stdout, level="TRACE", enqueue=True)
        else:
            logger.add(sys.stdout, level="DEBUG", enqueue=True)
    else:
        logger.add(sys.stdout, level="INFO", enqueue=True)
    logger.info("Starting {}...".format(prgname))

    v = Visualizer.Visualizer()
    p = Plotter.Plotter(dimx=[0, v.chunksize])
    """
    if v.open_stream() != 0:
        logger.critical("Stream couldn't be opened, exiting {}...".format(prgname))
        exit(1) # CONTINUE HERE
    """
    p.start_thread(v)
    logger.info("Quitting Application...")
    exit(0)