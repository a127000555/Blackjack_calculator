#include <Python.h>
#include <algorithm>
#include <iostream>
#include <vector>
#include <unordered_map>
#define STAND 0
#define HIT 1
using namespace std;

extern "C" {
    __declspec(dllexport) void mread(int16_t** input, size_t size)
    {
        cout << "Fucking raw" << endl;
        int i;
        int16_t* p = (int16_t*) malloc (size*sizeof(int16_t));
        for(i=0;i<size;i++) {
            p[i] = i*5;
        
        }
        *input = p;
    }
    __declspec(dllexport) void release(int16_t* input)
    {
        free(input);
    }
}