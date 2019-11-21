from loguru import logger
import sounddevice as sd
import pyaudio
import numpy as np


def print_available_devices():
    devices = sd.query_devices()
    for x in devices:
        logger.trace(x)
    """
    for i in range(0, self.p.get_device_count()):
        print("Name: {}".format(self.p.get_device_info_by_index(i)["name"]))
        print("Index: {}".format(self.p.get_device_info_by_index(i)["index"]))
    """


class Visualizer:
    chunk = np.empty(shape=(0, 0))
    stream = pyaudio.Stream
    multi = 4

    def __init__(self):
        logger.debug("Initiating Visualizer")
        self.p = pyaudio.PyAudio()
        dev_info = self.p.get_device_info_by_index(0)
        self.rate = 192000 #int(dev_info["defaultSampleRate"])
        self.format = pyaudio.paInt16
        self.chunksize = int(1024 * self.multi)
        self.deviceIndex = dev_info["index"]
        self.channels = 2
        print_available_devices()
        self.print_default_devices()
        self.defaultDevice = self.p.get_default_input_device_info()["index"]
        sd.default.device = self.defaultDevice
        sd.WasapiSettings(exclusive=True)
        if self.open_stream() != 0:
            logger.critical("Couldn't open Stream! Quitting application..")
            exit(1)
        self.stream.start()

    def print_default_devices(self):
        logger.trace("_"*50 + "DEFAULT_DEVICES" + "_"*50)
        dev_info = self.p.get_default_output_device_info()
        logger.trace("Default Output: \n{}".format(dev_info))
        dev_info = self.p.get_default_input_device_info()
        logger.trace("Default input: \n{}".format(dev_info))

    def get_chunk(self):
        # self.chunk = self.stream.read(self.chunksize)
        # logger.debug(self.chunk)
        self.chunk = self.stream.read(self.chunksize)
        return self.chunk

    def open_stream(self):
        logger.debug("Opening default output Stream")

        try:
            """
            self.stream = self.p.open(rate=self.rate,
                                      channels=self.channels,
                                      format=self.format,
                                      output=True,
                                      output_device_index=self.deviceIndex,
                                      frames_per_buffer=self.chunksize)
            """
            self.stream = sd.InputStream(samplerate=self.rate,
                                         blocksize=1 * self.chunksize,
                                         device=self.defaultDevice,
                                         channels=self.channels)

            logger.info("Connection to audio-stream established")
            return 0
        except(Exception):
            logger.exception('Warning encountered in function:')
            return 1
