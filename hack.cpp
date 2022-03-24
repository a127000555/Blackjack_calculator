// // #define PY_SSIZE_T_CLEAN
// // #include <Python.h>
#include <iostream>
#include <Python.h>

extern "C" {
    __declspec(dllexport) PyObject *foo(const char *);
    __declspec(dllexport) int sml(int);
}
int sml(int x)
{
    return x*2;
}


PyObject *foo(const char *filename)
{
    // setenv("PYTHONPATH", ".", 1);
    Py_Initialize();
    // PyRun_SimpleString("print(2**1000)");
    
    std::cout << "Oh " << filename << std::endl;
    PyObject *tuple;
    tuple = Py_BuildValue("(sss)", "Go", "Fuck", "Yourself"); 
    tuple = Py_BuildValue("(ddd)", 2.4, 5.0, 88.1); 
    // PyObject* args = Py_BuildValue("(dd)", 2.3, 4.1);
    // PyObject* pValue = Py_BuildValue("(s)", "XD");
    std::cout << "Oh shoot " << filename << std::endl;
    // list = Py_BuildValue("[iis]", 1, 2, "three");
    // PyObject* result = PyList_New(0);
    // int i;
    // for (i = 0; i < 100; ++i)
    // {
    //     PyList_Append(result, PyInt_FromLong(i));
    // }

    return tuple;
}


int main() {
    Py_Initialize();
    PyRun_SimpleString("print(2**1000)");

    std::cout << "Begin" << std::endl;
    PyObject* tuple = Py_BuildValue("(ss)", (char *)"XD", (char*)"Greg"); 
    PyObject* args = Py_BuildValue("(dd)", 2.3, 4.1);
    std::cout << "End" << std::endl;
}
/*
C:\mingw64\bin\g++.exe -I "C:\Python39\include" ./hack.cpp -o ./hack.exe -lpython3.9

*/