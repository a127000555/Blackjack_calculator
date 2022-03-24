@REM C:\mingw64\bin\g++.exe -shared -m64 -lstdc++ -Wl,-soname,myfunc.dll -o myfunc.dll foo.cpp

@REM C:\mingw64\bin\g++.exe -std=c++17 -O3 -I "C:\Python39\include" -I./h -g -fPIC -shared ./foo.cpp -o ./myfunc.dll -static-libgcc -static-libstdc++ -lpython3.9
C:\mingw64\bin\g++.exe ^
    -I "C:\Python39\include" ^
    -fPIC -shared ./hack.cpp ^
    -o ./hack.dll ^
    -LD "C:\Python39\libs\python39_d.lib" ^
    -lpython3.9 ^
    -static-libgcc ^
    -static-libstdc++ 

@REM g++ -I/usr/include/python3.6 hack.cpp -lpython3.6m -o hack.so -shared -fPIC

python test2.py