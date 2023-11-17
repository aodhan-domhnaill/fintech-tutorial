#include <iostream>

int Function(int num) 
{
    return num * 5;
}

extern "C" {
    int My_Function(int a)
    {
        return Function(a);
    }
}
