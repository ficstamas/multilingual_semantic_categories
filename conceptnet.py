import gzip
import contextlib
import json


class ConceptNetLoop:
    def __init__(self, fp):
        """
        Creates a generator for the content
        Parameters
        ----------
        fp
          File Pointer
        """
        self._fp = fp

    def __iter__(self):
        """
        Returns quadruplets of (relation, start, end, wight)
        Returns
        -------
            tuple
        """
        for line in self._fp:
            row = line.decode("utf-8").split("\t")
            yield row[1], row[2], row[3], json.loads(row[4])['weight']


class ConceptNet(contextlib.ContextDecorator):
    def __init__(self, path: str):
        """
        Iterates the compressed ConceptNet file
        Parameters
        ----------
        path
          Path to the compressed ConceptNet file
        """
        self._path = path
        self._fp = gzip.open(self._path, mode="r")

    def __enter__(self):
        """
        Returns an iterator
        Returns
        -------
            tuple
        """
        return ConceptNetLoop(self._fp)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._fp.close()
