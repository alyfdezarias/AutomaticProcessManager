import time
import sys

a = int(sys.argv[1])
b = int(sys.argv[2])
print(f"this is the process arg1={a}, it will wait {a*b} seconds")
time.sleep(a*b)