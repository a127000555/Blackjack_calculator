from ctypes import c_int16, c_int32, cdll, c_double, c_char_p, py_object
from os.path import abspath

# dll = ctypes.WinDLL(abspath('myfunc.dll'))
# print(dll)
# print(dll.timestwo(5))
# print(type(dll.testvector()))
# print(dll.testvector())
# print(dll.testvector())
# print(dll.testvector())
# print(dll.testvector())
# print(dll.testvector())


if True:
    from ctypes import WinDLL
    dll = WinDLL(abspath('hack.dll'))
else:
    dll = cdll.LoadLibrary(abspath('hack.so'))


dll.sml.argtypes = [c_int32]
dll.sml.restype = c_int32

dll.foo.argtypes = [c_char_p]
dll.foo.restype = py_object

# 設定 DLL 檔案中 foo 函數的傳回值資料型態
print(dll.sml(7))
a, b, c = dll.foo(b"hi\0")
print(a, b, c)
# print(dll.foo(b"hi"))
print("End")