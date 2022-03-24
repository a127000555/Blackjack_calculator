C:\mingw64\bin\g++.exe ^
    -std=c++17 ^
    -O3 -Ofast ^
    -I "C:\Python39\include" ^
    -o ./policy.dll ^
    -LD "C:\Python39\libs\python39_d.lib" ^
    -static-libgcc ^
    -static-libstdc++ ^
    -lpython3.9 ^
    -fPIC -shared ./policy.cpp

python burst_ev.py