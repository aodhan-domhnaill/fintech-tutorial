import support
import numpy as np

def test_support():
    mat1 = np.eye(3).astype(np.float32)
    mat2 = np.random.rand(3, 3).astype(np.float32)

    print(mat1)
    print(mat2)

    output_mat = support.My_Function(mat1, mat2)
    print(output_mat)
    assert np.isclose(support.My_Function(mat1, mat2), mat2).all()
