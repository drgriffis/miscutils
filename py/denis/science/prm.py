'''
Convenience class for storing and describing experimental results
'''

import numpy as np

class PersistentResultsMatrix:
    
    shape = None
    
    def __init__(self, *args, path=None):
        self.path = path
        self._results = np.ones(args) * -1
        self.shape = self._results.shape

    def __getitem__(self, key):
        return self._results[key]

    def __setitem__(self, key, value):
        self._results[key] = value

    def __repr__(self):
        return self._results.__repr__()

    def save(self, path=None):
        pth = path if path else self.path
        np.save(pth, self._results)

    @staticmethod
    def load(path, default_shape=(1,)):
        prm = PersistentResultsMatrix(*default_shape)
        try:
            prm._results = np.load(path)
            prm.shape = prm._results.shape
        except FileNotFoundError:
            pass
        prm.path = path
        return prm

    def apply(self, method):
        return method(self._results)

    def matr(self):
        return self._results.copy()

# shorthand
PRM = PersistentResultsMatrix
