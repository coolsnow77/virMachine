import timeit

from ctypes import cdll

def generate_c(num):
    libc = cdll.LoadLibrary("libc.so.6")
    while num:
        yield libc.rand() % 10
        num -= 1




print(timeit.timeit("sum(generate_c(999))", setup="from __main__ import generate_c", number=1000))




import timeit
from ctypes import cdll

def generate_c(num):
    #Load standard C library
    libc = cdll.LoadLibrary("libc.so.6") #Linux
    #libc = cdll.msvcrt #Windows
    while num:
        yield libc.rand() % 10
        num -= 1
    
print(timeit.timeit("sum(generate_c(999))", setup="from __main__ import generate_c", number=1000))

