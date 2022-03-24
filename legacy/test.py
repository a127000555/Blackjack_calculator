from ctypes import cdll
# w = open('C:\User?s/USER/Desktop/blackjack_prj/libfoo.so', 'rb').read()
# print(len(w))
lib = cdll.LoadLibrary('C:/Users/USER/Desktop/blackjack_prj/libfoo.so')

class Foo(object):
    def __init__(self):
        self.obj = lib.Foo_new()

    def bar(self):
        lib.Foo_bar(self.obj)

f = Foo()
f.bar() #and you will see "Hello" on the screen