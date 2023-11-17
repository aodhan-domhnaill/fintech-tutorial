import ctypes
import sys
import os 

# https://numpy.org/doc/stable/reference/generated/numpy.ndarray.ctypes.html
# https://numpy.org/doc/stable/reference/routines.ctypeslib.html

dir_path = os.path.dirname(os.path.realpath(__file__))
handle = ctypes.CDLL(dir_path + "/libsupport.so")     

handle.My_Function.argtypes = [ctypes.c_int] 

def My_Function(num):
    return handle.My_Function(num)
