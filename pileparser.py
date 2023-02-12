import os


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