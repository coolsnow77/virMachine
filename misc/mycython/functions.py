from ctypes import *

import time

libfunctions =cdll.LoadLibrary("./libfunctions.so")

def fibRec(n):
    if n < 2:
        return n
    else:
        return fibRec(n-1) + fibRec(n-2)

start =time.time()
fibRec(32)

finish = time.time()

print("python : " + str(finish - start))

# c Fibonacci

start = time.time()
x = libfunctions.fibRec(32)
finish  = time.time()

print ("C:" + str(finish - start))

