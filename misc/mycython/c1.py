import timeit
import random

def generate(num):
    while num:
        yield random.randrange(10)
        num -=1

def create_list(num):
    numbers = []
    while num:
        numbers.append(random.randrange(10))
        num -= 1
    return numbers


print(timeit.timeit("sum(generate(999))", setup="from __main__ import generate", number=1000))


print(timeit.timeit("sum(create_list(999))", setup="from __main__ import create_list", number=1000))


def testHello(oo):
    print "eeee"
    print "oooo"
