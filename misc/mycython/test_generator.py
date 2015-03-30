import timeit
print timeit.timeit("sum(generator.generate(999))", setup="import generator", number=1000)
