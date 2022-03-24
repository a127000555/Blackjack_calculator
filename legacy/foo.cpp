#include <stdio.h>
#include <vector>
#include <iostream>
#include <python.h>
#define PY_SSIZE_T_CLEAN
struct ret{
    int a=1, b=2, c=3;
};
extern "C" {
    __declspec(dllexport) int timestwo(int mynum)
    {
        std::vector<int> S;
        S.push_back(mynum);
        return S[0] * 3;
        // return mynum * 2;
    }
    __declspec(dllexport) ret testvector()
    {
        std::vector<int> S{1, 2, 3};

        return ret();
        // return mynum * 2;
    }
}

// class Foo
// {
// public:
//     void bar()
//     {
//         std::cout << "Hello" << std::endl;
//     }
// };
// extern "C"
// {
//     Foo *Foo_new() { return new Foo(); }
//     void Foo_bar(Foo *foo) { foo->bar(); }
// }

// extern "C"
// {
//     __declspec(dllexport) Foo *Foo_new() { return new Foo(); }
//     __declspec(dllexport) void Foo_bar(Foo *foo) { foo->bar(); }
// }

/*
c/Users/USER/Desktop/blackjack_prj
C:\mingw64\bin\g++.exe -c -fPIC foo.cpp -o foo.o
C:\mingw64\bin\g++.exe -shared -Wl,-soname,libfoo.so -o libfoo.so  foo.o

C:\mingw64\bin\gcc.exe -shared -o myfunc.dll foo.cpp

g++.exe -c -fPIC foo.cpp -o foo.o
g++.exe -shared -Wl,-soname,libfoo.so -o libfoo.so  foo.o


C:\mingw64\bin\g++.exe -shared -Wl,-soname,libfoo.so -o libfoo.so  foo.o


g++ -std=c++17 -O3  -I./h -g -fPIC -shared ./cpp/test.cpp -o ./libtest.dll -static-libgcc -static-libstdc++

*/