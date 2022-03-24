#include <stdio.h>
#include <Python.h>

int main(void) {
        Py_Initialize();
        PyObject *pName,*pName2, *pModule, *pFunc, *pArgs, *pValue;
        PySys_SetPath(L".");
        pName = PyUnicode_FromString((char*)"main");
        pModule = PyImport_Import(pName);
        pFunc = PyObject_GetAttrString(pModule, (char*)"main");
        pArgs = Py_BuildValue("(s)",(char *)"137912500");
        pValue = PyObject_CallObject(pFunc, pArgs);                  
        Py_Finalize();                                               
        printf("!!\n");
        // return;
}