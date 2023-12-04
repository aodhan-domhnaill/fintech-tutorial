#include <iostream>

int Function(int num) {
    return num * 5;
}

extern "C" {
    void My_Function(int dim1, int dim2, int dim3, float *mat1, float *mat2, float *output_mat) {
        for(int i = 0; i < dim1; i++) {
            for(int j =0; j < dim3; j++) {
                float sum = 0;
                for(int k =0; k < dim2; k++) {
                    sum += mat1[i * dim1 + k] * mat2[k * dim2 + j];
                }
                output_mat[i*dim1 + j] = sum; 
            }
        }
    }
}
