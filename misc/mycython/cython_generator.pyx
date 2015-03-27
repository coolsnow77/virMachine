#import random
# cython_generator.pyx

cdef extern from "stdlib.h":
    int c_libc_rand "rand"()

def generate(int num):
    while num:
        #yield random.randrange(10)
        yield c_libc_rand() % 10
        num -=1
