import ctypes
import sys
import os 
import numpy as np

# https://numpy.org/doc/stable/reference/generated/numpy.ndarray.ctypes.html
# https://numpy.org/doc/stable/reference/routines.ctypeslib.html

# numpy.ctypeslib.ndpointer(dtype=numpy.int32)

dir_path = os.path.dirname(os.path.realpath(__file__))
handle = ctypes.CDLL(dir_path + "/libsupport.so")     

handle.My_Function.argtypes = [ctypes.c_int, 
                               ctypes.c_int, 
                               ctypes.c_int, 
                               np.ctypeslib.ndpointer(dtype=np.float32), 
                               np.ctypeslib.ndpointer(dtype=np.float32), 
                               np.ctypeslib.ndpointer(dtype=np.float32)] 

def My_Function(mat1, mat2):
    output_mat = np.empty(shape=(mat1.shape[0], mat2.shape[1]), dtype=np.float32)
    assert mat1.shape[1] == mat2.shape[0]
    handle.My_Function(mat1.shape[0], 
                              mat2.shape[0], 
                              mat2.shape[1], 
                              mat1, 
                              mat2, 
                              output_mat)

    return output_mat
