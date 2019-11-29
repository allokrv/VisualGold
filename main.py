from loguru import logger
import Visualizer
import argparse
import Plotter
import time
import sys

prgname = "VisualGold"
vrs = "0.21"

# arg parser
apars = argparse.ArgumentParser(description="{} (Python3)".format(prgname))
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
    # still parsing args
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

    # create necessary objects
    v = Visualizer.Visualizer()
    p = Plotter.Plotter(dimx=[0, v.chunksize])

    p.start_thread(v)  # not a thread anymore but still starts program
    logger.info("Quitting Application...")
    exit(0)
