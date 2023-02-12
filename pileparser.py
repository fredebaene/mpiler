import logging
import os


# Instantiate a custom logger
logger = logging.getLogger(__main__)
logger.setLevel(level=logging.DEBUG)

# Instantiate a handler to log messages to stdout
c_handler = logging.StreamHandler()
c_handler.setLevel(level=logging.ERROR)
c_format = logging.Formatter("%(name)s - %(levelname)s : %(message)s")
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

class PileParser:

    def __init__(self, file_path, no_workers):
        # Initialize the attributes for the object
        self._file_path = file_path

        try:
            self._file_size = os.path.getsize(self._file_path)
        except FileNotFoundError as e:
            print(e)

        self._no_workers = no_workers
        self._chunk_bounds = []

    def get_chunks(self):
        self._file_size = os.path.getsize(self._file_path)
        mean_chunk_size = int(round(self._file_size / self._no_workers, 1))
        start = 0
        stop = mean_chunk_size
        f = open(self._file_path, "r")

        while start < self._file_size:
            f.seek(stop)
            if f.read(1) != "\n":
                f.readline()
            stop = f.tell() - 1
            self._chunk_bounds.append((start, stop))
            start = stop + 1
            stop = start + mean_chunk_size
            if stop > self._file_size:
                stop = self._file_size
        
        f.close()