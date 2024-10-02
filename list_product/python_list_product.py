import itertools
import sys
import time

v = range(int(sys.argv[1]))
reps = int(sys.argv[2])
start = time.perf_counter()
list(itertools.product(v, repeat=reps))
end = time.perf_counter()

print("list product en Python: ", end - start)

