from ctypes import *
from os.path import abspath
policy_dll = WinDLL(abspath('policy.dll'))
IntArray10 = c_int16 * 10
policy_dll.calculate_ev.argtypes = [IntArray10]
policy_dll.calculate_ev.restype = c_double

def get_ev(card_nums):
    p = IntArray10(*card_nums)
    ret = policy_dll.calculate_ev(p)
    return ret

card_nums = [24, 24, 24, 24, 24, 24, 24, 24, 24, 96]
print(get_ev(card_nums))