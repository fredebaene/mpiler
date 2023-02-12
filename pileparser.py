import logging
import os


# Instantiate a custom logger
logger = logging.getLogger(__name__)
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


    @property
    def file_path(self):
        return self._file_path

    @property
    def file_size(self):
        return self._file_size

    @property
    def no_workers(self):
        return self._no_workers

    @property
    def chunk_bounds(self):
        return self._chunk_bounds


    @no_workers.setter
    def no_workers(self, no_workers):
        if (
            isinstance(no_workers, int) and
            0 < no_workers <= os.cpu_count()
        ):
            self._no_workers = no_workers
        else:
            print(f"Invalid no. of cores: max. of {os.cpu_count()}")


    def get_chunks(self):

        # Compute the mean chunk size (in characters)
        self._file_size = os.path.getsize(self._file_path)
        mean_chunk_size = int(round(self._file_size / self._no_workers, 1))
        start = 0
        stop = mean_chunk_size

        # Open input file
        f = open(self._file_path, "r")
        logger.info("Determing bounds for chunks")

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
        logger.info(f"{self._file_path} is split into {len(self._chunk_bounds)} chunks")