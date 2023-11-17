import ctypes
import sys
import os 

# https://numpy.org/doc/stable/reference/generated/numpy.ndarray.ctypes.html
# https://numpy.org/doc/stable/reference/routines.ctypeslib.html
class Support:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.handle = ctypes.CDLL(dir_path + "/support.so")     

        self.handle.My_Function.argtypes = [ctypes.c_int] 

    def My_Function(self, num):
        return self.handle.My_Function(num)
